import os
import sys
import uuid
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / "env", override=True)
load_dotenv(PROJECT_ROOT / ".env", override=True)

try:
    from src.api.client import ZernioClient
except ImportError as e:
    print(f"Error importing Zernio client: {e}")
    sys.exit(1)


def _idea_template(bucket, angle, evidence_quotes, why_good_idea, suggested_angle, platform):
    """Create a normalized idea payload expected by IdeasTab."""
    return {
        "id": str(uuid.uuid4()),
        "platform": platform,
        "bucket": bucket,
        "angle": angle,
        "evidence_quotes": evidence_quotes,
        "why_good_idea": why_good_idea,
        "suggested_angle": suggested_angle,
    }


def _build_default_ideas(platform):
    """Fallback ideas used when external generation is not available."""
    if platform == "youtube":
        return [
            _idea_template(
                "comments",
                "Los 3 bloqueos al hablar en camara que casi nadie reconoce",
                [
                    "'Me quedo en blanco cuando grabo'",
                    "'Repito 20 tomas y ninguna me convence'",
                ],
                "Responde dolores frecuentes y fomenta guardados por valor practico.",
                "Formato lista con ejemplo real + mini ejercicio de 60 segundos.",
                platform,
            ),
            _idea_template(
                "dms",
                "Como entrenar presencia en 7 dias sin sonar forzada",
                [
                    "'Quiero sonar natural pero con autoridad'",
                    "'Necesito estructura para practicar'",
                ],
                "Conecta con intencion de compra porque ofrece una ruta clara.",
                "Video educativo con calendario descargable en descripcion.",
                platform,
            ),
            _idea_template(
                "top_content",
                "El error de oratoria que te hace parecer menos experta",
                [
                    "'Hablo rapido cuando estoy nerviosa'",
                    "'Siento que no transmito seguridad'",
                ],
                "Tema con alto potencial de clic por promesa de mejora inmediata.",
                "Abrir con demo antes/despues y cerrar con CTA a diagnostico.",
                platform,
            ),
        ]

    return [
        _idea_template(
            "comments",
            "5 frases que debilitan tu mensaje sin darte cuenta",
            [
                "'Perdon si me explico mal'",
                "'No soy experta pero...'",
            ],
            "Ayuda a tu audiencia a identificar patrones y aplicarlo de inmediato.",
            "Carrusel con ejemplo de reemplazo frase por frase.",
            platform,
        ),
        _idea_template(
            "dms",
            "Tu perfil comunicativo segun Eneagrama en 1 minuto",
            [
                "'No se como explicar a que me dedico'",
                "'Siento que mi voz no refleja mi valor'",
            ],
            "Une diferenciador de marca con formato corto y compartible.",
            "Reel tipo test rapido + CTA a palabra clave PERFIL.",
            platform,
        ),
        _idea_template(
            "top_content",
            "El ritual de 3 pasos para hablar con seguridad antes de grabar",
            [
                "'Me tiembla la voz al empezar'",
                "'No se como calmar nervios'",
            ],
            "Combina neurociencia + accion concreta, ideal para guardados.",
            "Video demostrativo con temporizador y cierre inspiracional.",
            platform,
        ),
    ]

async def generate_all_ideas_ig():
    """Generate all Instagram ideas."""
    # TODO: Replace with Claude flow when integration is ready.
    return _build_default_ideas("instagram")

def generate_all_ideas_yt():
    """Generate all YouTube ideas."""
    # TODO: Replace with Claude flow when integration is ready.
    return _build_default_ideas("youtube")

def discard_idea(idea_id, reason_quick, reason_text):
    """Discard an idea"""
    # This would be implemented with actual logic to store discarded ideas
    print(f"Discarding idea {idea_id} with reason: {reason_quick} - {reason_text}")
    return True

# For compatibility with app.py imports
generate_ideas = generate_all_ideas_ig