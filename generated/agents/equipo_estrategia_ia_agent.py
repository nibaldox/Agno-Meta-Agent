"""
Equipo Estrategia IA - Equipo de Agentes AI colaborativos.

Rol: Un equipo colaborativo que analiza datos, investiga tendencias y propone estrategias de adopción de IA
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

    # Miembro: Analista de Datos
    miembro_0 = Agent(
        name="Analista de Datos",
        role="Analizar información disponible y extraer tendencias",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[ReasoningTools(add_instructions=True)],
    )

    # Miembro: Investigador
    miembro_1 = Agent(
        name="Investigador",
        role="Buscar documentación e investigaciones relevantes",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True)],
    )

    # Miembro: Coordinador
    miembro_2 = Agent(
        name="Coordinador",
        role="Integrar hallazgos y proponer un plan de acción",
        model=DeepSeek(id="deepseek-reasoner"),
        tools=[ReasoningTools(add_instructions=True)],
    )

    member_info = [
        ("Analista de Datos", "Analizar datasets y extraer tendencias"),
        ("Investigador", "Buscar documentación e investigaciones relevantes"),
        ("Coordinador", "Integrar hallazgos y proponer un plan de acción")
    ]

    team = Team(
        name="Equipo Estrategia IA",
        members=[miembro_0, miembro_1, miembro_2],
        model=DeepSeek(id="deepseek-reasoner"),
        instructions=[
        "Coordinen hallazgos y propongan un plan breve",
        "Limiten la respuesta a 3 recomendaciones concretas",
        "Eviten cargar datasets locales; basen el análisis en conocimiento general y búsqueda web"
        ],
        markdown=True,
    )

    print("\nEquipo Estrategia IA está listo\n")
    print("Miembros del equipo:")
    for display_name, display_role in member_info:
        print(f"  - {display_name}: {display_role}")

    print("\nEjemplo de tarea: Diseñen una estrategia de IA para una compañía fintech\n")

    resultado = team.run("Diseñen una estrategia de IA para una compañía fintech")
    print("\nResultado del equipo:\n")
    print(resultado)

    print("\n")
    print("El equipo colabora automáticamente para completar tareas complejas.")


if __name__ == "__main__":
    main()
