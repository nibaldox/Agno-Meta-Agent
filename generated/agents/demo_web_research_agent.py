"""
Demo Web Research Agent - Agente AI generado automáticamente.

Rol: Buscar noticias recientes sobre inteligencia artificial
Herramientas: duckduckgo
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el agente."""

    # Crear el agente
    agent = Agent(
        name="Demo Web Research Agent",
        role="Buscar noticias recientes sobre inteligencia artificial",
        model=DeepSeek(id="deepseek-chat"),
        tools=[DuckDuckGoTools()],
        instructions=[
        "Saluda al usuario de forma cordial",
        "Usa la herramienta de búsqueda web para obtener la información",
        "Resume la noticia destacando la fecha y la fuente"
        ],
        markdown=True,
    )

    # Ejemplo de uso
    print("\n🤖 Demo Web Research Agent está listo\n")
    print("Ejemplo de pregunta: ¿Qué hay de nuevo en IA hoy?\n")

    # Ejecutar con el ejemplo
    agent.print_response("¿Qué hay de nuevo en IA hoy?", stream=True)

    print("\n")
    print("Para usar interactivamente, modifica este archivo y usa agent.print_response(tu_pregunta)")


if __name__ == "__main__":
    main()
