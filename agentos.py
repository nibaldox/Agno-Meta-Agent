"""
AgentOS - Meta-Agente Generador de Agentes AI

Este es el servidor AgentOS que expone los agentes del sistema:
- Analyzer Agent: Analiza solicitudes y hace preguntas aclaratorias
- Planner Agent: Crea planes estructurados de agentes
- Meta Agent API: Endpoints custom para generación de código

Endpoints principales:
- GET /health - Health check
- GET /config - Configuración del OS
- POST /agents/{agent_id}/chat - Chat con agentes
- GET /sessions - Listar sesiones
- POST /api/meta-agent/generate - Generar código de agente
"""

import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.storage.agent import SqliteAgentStorage

from src.application.services.meta_agent import AgentPlan

# Cargar variables de entorno
load_dotenv()

# Configurar modelos
analysis_model = DeepSeek(id="deepseek-chat")
planning_model = DeepSeek(id="deepseek-reasoner")

# Agente Analyzer: Analiza solicitudes y hace preguntas aclaratorias
analyzer_agent = Agent(
    name="Analyzer Agent",
    role="Analizar solicitudes de usuarios y hacer preguntas aclaratorias",
    model=analysis_model,
    instructions=[
        "Analiza la solicitud del usuario para crear un agente AI",
        "Identifica qué información falta para crear un agente completo",
        "Haz preguntas específicas y contextuales",
        "Si tienes toda la información necesaria, responde exactamente: INFO_COMPLETA",
        "Sé conciso y amigable en tus preguntas",
        "Cuando el usuario responda, integra su información al contexto",
        "Sugiere opciones concretas cuando sea posible (ej: herramientas disponibles)",
    ],
    markdown=True,
    show_tool_calls=False,
)

# Agente Planner: Crea planes estructurados
planner_agent = Agent(
    name="Planner Agent",
    role="Crear planes estructurados para agentes AI",
    model=planning_model,
    instructions=[
        "Crea un plan detallado en formato JSON",
        "Usa el esquema AgentPlan proporcionado",
        "Infiere información razonable si no está explícita",
        "Sé específico en rol, instrucciones y herramientas",
        "Retorna SOLO el JSON, sin texto adicional ni markdown",
        "Asegura que el JSON sea válido y completo",
    ],
    markdown=False,
    show_tool_calls=False,
    response_model=AgentPlan,
)

# Storage compartido para persistencia
storage = SqliteAgentStorage(
    table_name="agentos_sessions",
    db_file="agents_memory.sqlite"
)

# Crear AgentOS
agent_os = AgentOS(
    os_id="meta-agent-os-v1",
    description="Meta-Agente Generador de Agentes AI con AgentOS",
    agents=[analyzer_agent, planner_agent],
    storage=storage,
)

# Añadir rutas custom para generación de código
from src.infrastructure.api.meta_routes import router as meta_router
agent_os.app.include_router(meta_router, prefix="/api/meta-agent", tags=["Meta-Agent"])

# CORS para desarrollo (permitir Lantui conectarse desde localhost)
from fastapi.middleware.cors import CORSMiddleware
agent_os.app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serve_agentos():
    """Inicia el servidor AgentOS."""
    import uvicorn
    
    print("\n" + "="*60)
    print("🤖 Meta-Agente AgentOS iniciando...")
    print("="*60)
    print("\n📍 Endpoints disponibles:")
    print("  • API:          http://localhost:7777")
    print("  • Docs:         http://localhost:7777/docs")
    print("  • Config:       http://localhost:7777/config")
    print("  • Health:       http://localhost:7777/health")
    print("\n🔧 Agentes activos:")
    print("  • Analyzer Agent (analyzer_agent)")
    print("  • Planner Agent (planner_agent)")
    print("\n🚀 Endpoints custom:")
    print("  • POST /api/meta-agent/generate")
    print("  • POST /api/meta-agent/generate-stream")
    print("  • GET  /api/meta-agent/generated")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        "agentos:app",
        host="0.0.0.0",
        port=7777,
        reload=True,
        reload_dirs=["src", "."],
    )


# Exponer la app FastAPI para uvicorn
app = agent_os.app


if __name__ == "__main__":
    serve_agentos()

