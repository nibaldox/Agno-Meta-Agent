"""Genera un equipo de agentes colaborativos de nivel superior."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.application.services.meta_agent import AgentPlan, MetaAgent


def main() -> None:
    """Genera un equipo de agentes especializados para un objetivo complejo."""

    miembros_equipo = [
        {
            "nombre": "Analista de Datos",
            "rol": "Analizar datasets y extraer tendencias",
            "herramientas": ["python"],
        },
        {
            "nombre": "Investigador",
            "rol": "Buscar documentación e investigaciones relevantes",
            "herramientas": ["duckduckgo", "reasoning"],
        },
        {
            "nombre": "Coordinador",
            "rol": "Integrar hallazgos y proponer un plan de acción",
            "herramientas": ["reasoning"],
        },
    ]

    plan = AgentPlan(
        nombre="Equipo Estrategia IA",
        rol=(
            "Un equipo colaborativo que analiza datos, investiga tendencias y"
            " propone estrategias de adopción de IA"
        ),
        modelo="deepseek-reasoner",
        nivel=4,
        herramientas=[],
        instrucciones=[
            "Coordinen los hallazgos entre analista, investigador y coordinador",
            "Entreguen un plan con acciones a corto, mediano y largo plazo",
        ],
        necesita_memoria=False,
        es_equipo=True,
        miembros_equipo=miembros_equipo,
        ejemplo_uso="Diseñen una estrategia de IA para una compañía fintech",
    )

    meta_agent = MetaAgent()
    code = meta_agent.generate_code(plan)

    output_path = Path("generated/agents/equipo_estrategia_ia_agent.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")

    print("Equipo de agentes generado (Estrategia IA)")
    print(f"Archivo: {output_path.resolve()}")


if __name__ == "__main__":
    main()

