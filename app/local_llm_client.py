import asyncio
from typing import Optional, Dict, Any
import httpx
import time

# Excepción personalizada para errores del LLM local
class LocalLLMError(Exception):
    """Excepción lanzada cuando ocurre un error en la comunicación con el LLM local"""
    pass


class LocalLLMClient:
    """Cliente asincrónico para interactuar con el modelo local LLM a través de llama.cpp"""
    
    def __init__(
        self,
        endpoint: str,
        model: str,
        max_tokens: int,
        temperature: float,
        timeout: int = 30
    ):
        """
        Inicializa el cliente del LLM local
        
        Args:
            endpoint: URL del endpoint de completions del modelo local
            model: Nombre del modelo a usar
            max_tokens: Máximo número de tokens en la respuesta
            temperature: Temperatura para el muestreo (0.0 a 1.0)
            timeout: Tiempo máximo de espera en segundos
        """
        self.endpoint = endpoint
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)
    
    async def __aenter__(self):
        """Context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self._client.aclose()
    
    async def _make_request_with_retry(
        self,
        payload: Dict[str, Any],
        max_retries: int = 3
    ) -> httpx.Response:
        """
        Realiza una solicitud con retry y backoff exponencial
        
        Args:
            payload: Payload para la solicitud al endpoint
            max_retries: Número máximo de reintentos
            
        Returns:
            Respuesta HTTP del servidor
            
        Raises:
            LocalLLMError: Si se agotan los intentos o ocurre un error no recuperable
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                response = await self._client.post(
                    self.endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                # Verificar si la respuesta es exitosa
                if response.status_code < 400:
                    return response
                else:
                    # Para errores 4xx, no reintentar (excepto 429)
                    if response.status_code != 429:
                        raise LocalLLMError(
                            f"HTTP {response.status_code}: {response.text}"
                        )
                    elif attempt == max_retries:
                        raise LocalLLMError(
                            f"HTTP {response.status_code} después de {max_retries} intentos"
                        )
                    
            except httpx.RequestError as e:
                # Errores de red, reintentar
                last_exception = e
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Backoff exponencial
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise LocalLLMError(f"Error de red después de {max_retries} intentos: {e}")
            
            except Exception as e:
                # Otros errores, reintentar si no es el último intento
                last_exception = e
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Backoff exponencial
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise LocalLLMError(f"Error desconocido después de {max_retries} intentos: {e}")
        
        # Si llegamos aquí, todos los intentos fallaron
        if last_exception:
            raise LocalLLMError(f"Todos los intentos fallidos: {last_exception}")
        else:
            raise LocalLLMError("Todos los intentos fallidos")
    
    async def generate_text(
        self,
        messages: list[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Genera texto usando el modelo local
        
        Args:
            messages: Lista de mensajes para el modelo (formato ChatML)
            system_prompt: Prompt del sistema opcional
            
        Returns:
            Texto generado por el modelo
            
        Raises:
            LocalLLMError: Si ocurre un error durante la generación
        """
        # Construir el payload para la solicitud
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": False
        }
        
        # Añadir system prompt si se proporciona
        if system_prompt:
            payload["messages"] = [
                {"role": "system", "content": system_prompt}
            ] + payload["messages"]
        
        try:
            response = await self._make_request_with_retry(payload)
            response.raise_for_status()
            
            # Extraer el texto generado de la respuesta
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except httpx.HTTPStatusError as e:
            raise LocalLLMError(f"Error HTTP {e.response.status_code}: {e.response.text}")
        except KeyError as e:
            raise LocalLLMError(f"Formato de respuesta inválido del modelo: {e}")
        except Exception as e:
            raise LocalLLMError(f"Error al procesar la respuesta del modelo: {e}")