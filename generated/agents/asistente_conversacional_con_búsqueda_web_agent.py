"""
Asistente Conversacional con Búsqueda Web - Agente AI con memoria persistente.

Rol: Agente conversacional que responde preguntas de contexto general utilizando búsqueda web en múltiples fuentes (DuckDuckGo y Serper) y mantiene memoria de conversaciones previas
Herramientas: duckduckgo, serper
Memoria: Activada (SQLite)
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.serper import SerperTools

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el agente con memoria."""

    # Configurar storage
    db = SqliteDb(db_file="agents_memory.sqlite")

    # Crear el agente
    agent = Agent(
        name="Asistente Conversacional con Búsqueda Web",
        role="Agente conversacional que responde preguntas de contexto general utilizando búsqueda web en múltiples fuentes (DuckDuckGo y Serper) y mantiene memoria de conversaciones previas",
        model=DeepSeek(id="deepseek-chat"),
        tools=[DuckDuckGoTools(), SerperTools(api_key=os.getenv("SERPER_API_KEY"))],
        instructions=[
        "Iniciar conversaciones de manera amigable y natural",
        "Responder preguntas sobre cualquier tema de contexto general",
        "Utilizar búsqueda web con DuckDuckGo y Serper para obtener información precisa y actualizada",
        "Mantener el contexto de conversaciones previas para proporcionar respuestas coherentes",
        "No tener restricciones en los temas discutidos, pero mantener un tono respetuoso",
        "Priorizar fuentes confiables en las búsquedas y verificar información cuando sea necesario"
        ],
        db=db,
        markdown=True,
        enable_user_memories=True,
        enable_session_summaries=True,
    )

    # Ejemplo de uso
    print("\n🤖 Asistente Conversacional con Búsqueda Web está listo (con memoria)\n")
    print("Ejemplo de pregunta: Usuario: ¿Cuál es la capital de Francia? Agente: La capital de Francia es París. Usuario: ¿Y qué sabes sobre su historia? Agente: París tiene una historia rica que se remonta a más de 2000 años... [usando búsqueda web para detalles históricos]\n")

    # Ejecutar con el ejemplo
    agent.print_response("Usuario: ¿Cuál es la capital de Francia? Agente: La capital de Francia es París. Usuario: ¿Y qué sabes sobre su historia? Agente: París tiene una historia rica que se remonta a más de 2000 años... [usando búsqueda web para detalles históricos]", stream=True)

    print("\n")
    print("💾 Las conversaciones se guardan en: agents_memory.sqlite")
    print("El agente recordará contexto de sesiones anteriores.")


if __name__ == "__main__":
    main()
