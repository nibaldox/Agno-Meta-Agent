"""
Buscador de Noticias Tech - Agente AI con memoria persistente.

Rol: Agente especializado en buscar, analizar y resumir noticias de tecnología en tiempo real, adaptándose a las preferencias del usuario mediante memoria de interacciones previas
Herramientas: duckduckgo, reasoning, file
Memoria: Activada (SQLite)
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory.agent import AgentMemory
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el agente con memoria."""

    # Configurar storage
    db = SqliteDb(db_file="agents_memory.sqlite")

    # Crear el agente
    agent = Agent(
        name="Buscador de Noticias Tech",
        role="Agente especializado en buscar, analizar y resumir noticias de tecnología en tiempo real, adaptándose a las preferencias del usuario mediante memoria de interacciones previas",
        model=DeepSeek(id="deepseek-chat"),
        tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True), FileTools()],
        instructions=[
        "Buscar noticias de tecnología en tiempo real usando múltiples fuentes",
        "Priorizar fuentes confiables como TechCrunch, Wired, The Verge, y medios especializados",
        "Generar resúmenes diarios concisos pero informativos",
        "Recordar las preferencias del usuario sobre temas, empresas y tipos de noticias",
        "Aprender del feedback del usuario para mejorar futuras búsquedas",
        "Organizar las noticias por relevancia e importancia",
        "Incluir enlaces a las fuentes originales para consulta adicional",
        "Mantener un tono profesional pero accesible en los resúmenes",
        "Actualizar la base de conocimiento con nuevas preferencias detectadas"
        ],
        db=db,
        markdown=True,
        enable_user_memories=True,
        enable_session_summary=True,
    )

    # Ejemplo de uso
    print("\n🤖 Buscador de Noticias Tech está listo (con memoria)\n")
    print("Ejemplo de pregunta: Usuario: '¿Cuáles son las noticias más importantes de tecnología hoy?' - El agente buscará noticias actuales, generará un resumen organizado por relevancia, recordará preferencias previas y proporcionará enlaces a las fuentes.\n")

    # Ejecutar con el ejemplo
    agent.print_response("Usuario: '¿Cuáles son las noticias más importantes de tecnología hoy?' - El agente buscará noticias actuales, generará un resumen organizado por relevancia, recordará preferencias previas y proporcionará enlaces a las fuentes.", stream=True)

    print("\n")
    print("💾 Las conversaciones se guardan en: agents_memory.sqlite")
    print("El agente recordará contexto de sesiones anteriores.")


if __name__ == "__main__":
    main()
