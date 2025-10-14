"""
Equipo de Creación de Artículos de IA - Equipo de Agentes AI colaborativos.

Rol: Crear artículos de alta calidad sobre tecnología e inteligencia artificial, optimizados para SEO, con un estilo mixto (técnico y accesible)
Miembros: 3
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el equipo de agentes."""

    # Crear miembros del equipo

    # Miembro: Investigador de IA
    investigador_de_ia = Agent(
        name="Investigador de IA",
        role="Buscar información actualizada y relevante sobre tecnología e inteligencia artificial usando búsqueda web y análisis de archivos",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[DuckDuckGoTools(), FileTools()],
    )

    # Miembro: Redactor de Contenido
    redactor_de_contenido = Agent(
        name="Redactor de Contenido",
        role="Escribir artículos atractivos y bien estructurados con estilo mixto (técnico pero accesible)",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[FileTools(), ReasoningTools(add_instructions=True)],
    )

    # Miembro: Especialista SEO
    especialista_seo = Agent(
        name="Especialista SEO",
        role="Optimizar el contenido para motores de búsqueda, incluyendo keywords, meta descripciones y estructura",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[ReasoningTools(add_instructions=True)],
    )

    # Crear el equipo
    team = Team(
        name="Equipo de Creación de Artículos de IA",
        members=[investigador_de_ia, redactor_de_contenido, especialista_seo],
        model=DeepSeek(id="deepseek-reasoner"),
        instructions=[
        "Coordinar entre investigadores, redactores y editores SEO para producir artículos completos",
        "Asegurar que el contenido sea preciso, actualizado y atractivo para el público objetivo",
        "Mantener un estilo mixto: técnico para quienes tienen conocimientos, pero accesible para principiantes",
        "Optimizar todos los artículos para SEO, incluyendo palabras clave, meta descripciones y estructura",
        "Utilizar la memoria para recordar preferencias de estilo, temas ya cubiertos y evitar repeticiones"
        ],
        markdown=True,
    )

    # Ejemplo de uso
    print("\n🤖 Equipo de Creación de Artículos de IA está listo\n")
    print("Miembros del equipo:")
    print("  - Investigador de IA: Buscar información actualizada y relevante sobre tecnología e inteligencia artificial usando búsqueda web y análisis de archivos")
    print("  - Redactor de Contenido: Escribir artículos atractivos y bien estructurados con estilo mixto (técnico pero accesible)")
    print("  - Especialista SEO: Optimizar el contenido para motores de búsqueda, incluyendo keywords, meta descripciones y estructura")
    print("\nEjemplo de tarea: Crear un artículo sobre las implicaciones éticas de la IA, incluyendo investigación actual, redacción en estilo mixto y optimización SEO para términos como 'ética IA'.\n")

    # Ejecutar con el ejemplo
    team.print_response("Crear un artículo sobre las implicaciones éticas de la IA, incluyendo investigación actual, redacción en estilo mixto y optimización SEO para términos como 'ética IA'.", stream=True)

    print("\n")
    print("El equipo colabora automáticamente para completar tareas complejas.")


if __name__ == "__main__":
    main()
