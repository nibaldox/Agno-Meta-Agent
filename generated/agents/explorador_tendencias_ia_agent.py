"""
Explorador de Tendencias IA - Agente AI generado automáticamente.

Rol: Investigar un tema de inteligencia artificial y entregar puntos clave, incluyendo enlaces relevantes
Herramientas: duckduckgo, reasoning
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el agente."""

    # Crear el agente
    agent = Agent(
        name="Explorador de Tendencias IA",
        role="Investigar un tema de inteligencia artificial y entregar puntos clave, incluyendo enlaces relevantes",
        model=DeepSeek(id="deepseek-chat"),
        tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True)],
        instructions=[
        "Pregunta al usuario cuál es el tema específico dentro de la IA",
        "Realiza una búsqueda rápida sobre el tema",
        "Resume tres hallazgos clave con fuente y fecha"
        ],
        markdown=True,
    )

    # Ejemplo de uso
    print("\n🤖 Explorador de Tendencias IA está listo\n")
    print("Ejemplo de pregunta: Explora el estado actual del aprendizaje federado\n")

    # Ejecutar con el ejemplo
    agent.print_response("Explora el estado actual del aprendizaje federado", stream=True)

    print("\n")
    print("Para usar interactivamente, modifica este archivo y usa agent.print_response(tu_pregunta)")


if __name__ == "__main__":
    main()
