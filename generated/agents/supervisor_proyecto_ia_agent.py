"""
Supervisor de Proyecto IA - Agente AI con memoria persistente.

Rol: Dar seguimiento a tareas de un proyecto de inteligencia artificial, guardando decisiones y próximos pasos
Herramientas: duckduckgo, file
Memoria: Activada (SQLite)
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el agente con memoria."""

    # Configurar storage
    db = SqliteDb(db_file="agents_memory.sqlite")

    # Crear el agente
    agent = Agent(
        name="Supervisor de Proyecto IA",
        role="Dar seguimiento a tareas de un proyecto de inteligencia artificial, guardando decisiones y próximos pasos",
        model=DeepSeek(id="deepseek-chat"),
        tools=[DuckDuckGoTools(), FileTools()],
        instructions=[
        "Registra cada tarea discutida con fecha y responsable",
        "Verifica si hay dependencias o bloqueos",
        "Sugiere próximos pasos basados en la memoria almacenada"
        ],
        db=db,
        markdown=True,
        enable_user_memories=True,
        enable_session_summary=True,
    )

    # Ejemplo de uso
    print("\n🤖 Supervisor de Proyecto IA está listo (con memoria)\n")
    print("Ejemplo de pregunta: Revisa el estado de la integración con API externas\n")

    # Ejecutar con el ejemplo
    agent.print_response("Revisa el estado de la integración con API externas", stream=True)

    print("\n")
    print("💾 Las conversaciones se guardan en: agents_memory.sqlite")
    print("El agente recordará contexto de sesiones anteriores.")


if __name__ == "__main__":
    main()
