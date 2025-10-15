"""
Equipo Analitico - Equipo de Agentes AI colaborativos.

Rol: Resolver tareas
Miembros: 3
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el equipo de agentes."""

    # Crear miembros del equipo

    # Miembro: Researcher
    miembro_0 = Agent(
        name="Researcher",
        role="Buscar información",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[DuckDuckGoTools()],
    )

    # Miembro: Analyzer
    miembro_1 = Agent(
        name="Analyzer",
        role="Analizar datos",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[ReasoningTools(add_instructions=True)],
    )

    # Miembro: Writer
    miembro_2 = Agent(
        name="Writer",
        role="Escribir respuestas",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[],
    )

    # Crear el equipo
    team = Team(
        name="Equipo Analitico",
        members=[miembro_0, miembro_1, miembro_2],
        model=DeepSeek(id="deepseek-reasoner"),
        instructions=[
        "Colaboren efectivamente",
        "Dividan el trabajo según especialidades",
        "Combinen sus hallazgos"
        ],
        markdown=True,
    )

    # Ejemplo de uso
    print("
🤖 Equipo Analitico está listo
")
    print("Miembros del equipo:")
    print("  - Researcher: Buscar información")
    print("  - Analyzer: Analizar datos")
    print("  - Writer: Escribir respuestas")
    print("
Ejemplo de tarea: test
")

    # Ejecutar con el ejemplo
    team.print_response("test", stream=True)

    print("
")
    print("El equipo colabora automáticamente para completar tareas complejas.")


if __name__ == "__main__":
    main()
