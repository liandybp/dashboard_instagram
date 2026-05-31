Documento de Contexto Técnico: Integración con Zernio API
1. Resumen General
Zernio es una API unificada para la gestión de redes sociales que soporta más de 14 plataformas (Instagram, Facebook, Twitter/X, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Bluesky, Threads, Google Business Profile, Telegram, Snapchat, WhatsApp y Discord)
. La arquitectura se basa en tres conceptos clave:
Profiles: Contenedores para agrupar cuentas por marca o proyecto
.
Accounts: Cuentas sociales individuales conectadas mediante OAuth o credenciales
.
Posts: Contenido programable o inmediato hacia múltiples plataformas simultáneamente
.
2. Capacidades de Desarrollo por Módulo
A. Publicación y Contenido
Formatos Soportados: Posts estándar, Carruseles (hasta 10 elementos), Stories, Reels y Shorts
.
Funciones Avanzadas: Etiquetado de usuarios (coordenadas x,y), invitación de colaboradores, primer comentario automático, encuestas (Twitter/Discord) y configuración de privacidad
.
Optimización: Compresión automática de medios que exceden límites de plataforma y pre-validación de longitud de texto
.
B. Analíticas y Datos (Add-on requerido para históricos)
Métricas de Post: Impresiones, alcance, likes, comentarios, compartidos, guardados y clics
.
Métricas de Cuenta: Alcance diario, total de interacciones y historial de seguidores (Zernio reconstruye datos que plataformas como Meta ya no entregan de forma nativa)
.
Inteligencia de Datos: Endpoints para determinar los mejores momentos para publicar, el decaimiento de rendimiento del contenido y la relación entre frecuencia de posteo y engagement
.
C. Inbox y CRM (Unified Messaging)
Mensajería: Listar conversaciones, enviar texto/adjuntos y gestionar estados de lectura/entrega
.
Contexto de Audiencia: Datos de perfil del remitente (si es seguidor, conteo de seguidores, estado de verificación)
.
Moderación: Gestión de comentarios (responder, ocultar, eliminar) y reseñas en Google Business y Facebook
.
D. Automatización y Workflows
Workflows: API para construir flujos de conversación basados en grafos de nodos/aristas
.
Comment-to-DM: Automatización para enviar mensajes directos basados en palabras clave en comentarios
.
Broadcasts y Secuencias: Envío masivo de mensajes (WhatsApp/Telegram) y campañas de goteo (drip campaigns)
.
E. Publicidad (Ads)
Integración unificada para crear, gestionar y analizar campañas en Meta Ads, Google Ads, TikTok Ads, LinkedIn Ads, Pinterest Ads y X Ads
.
Soporte para Conversions API (eventos offline) y gestión de audiencias personalizadas/lookalikes
.
3. Infraestructura Técnica para el Plan de Desarrollo
Autenticación: Mediante API Keys con prefijo sk_ enviadas como Bearer Token
.
Webhooks: Sistema de notificaciones en tiempo real para eventos de publicación, recepción de mensajes, cambios en anuncios y nuevas reseñas
.
Protocolo MCP: Zernio ofrece un servidor Model Context Protocol (MCP) en https://mcp.zernio.com/mcp. Esto permite que Claude ejecute herramientas de la API directamente si se configura como conector
.
Validación: Herramientas para verificar URLs de medios y límites de caracteres antes del envío
.
SDKs: Disponibles en Node.js, Python, Go, Ruby, Java, PHP, .NET y Rust
.
4. Limitaciones Importantes a Considerar
Límites de Velocidad: Varían según el número de cuentas conectadas (desde 60 hasta 1,200 req/min)
.
Plataformas Específicas: Twitter/X requiere cargos por llamada API pasados directamente al usuario; Instagram requiere cuentas Business/Creator; Bluesky usa contraseñas de aplicación
.
Medios: No se permiten enlaces de Google Drive o Dropbox como URLs de medios; deben ser links directos a archivos o subidos mediante el endpoint de carga de Zernio
.

--------------------------------------------------------------------------------
Sugerencia para Claude: "Basándote en estos puntos, por favor crea un plan de desarrollo para [Tu Objetivo del Dashboard], priorizando el uso de webhooks para la reactividad y los endpoints de analíticas agregadas para los gráficos de rendimiento."