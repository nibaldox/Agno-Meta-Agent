"""Genera un agente con memoria persistente y herramientas adicionales."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.application.services.meta_agent import AgentPlan, MetaAgent


def main() -> None:
    """Genera un agente con memoria para seguimiento de proyectos."""

    plan = AgentPlan(
        nombre="Supervisor de Proyecto IA",
        rol=(
            "Dar seguimiento a tareas de un proyecto de inteligencia artificial,"
            " guardando decisiones y próximos pasos"
        ),
        modelo="deepseek-chat",
        nivel=3,
        herramientas=["duckduckgo", "file"],
        instrucciones=[
            "Registra cada tarea discutida con fecha y responsable",
            "Verifica si hay dependencias o bloqueos",
            "Sugiere próximos pasos basados en la memoria almacenada",
        ],
        necesita_memoria=True,
        es_equipo=False,
        miembros_equipo=[],
        ejemplo_uso="Revisa el estado de la integración con API externas",
    )

    meta_agent = MetaAgent()
    code = meta_agent.generate_code(plan)

    output_path = Path("generated/agents/supervisor_proyecto_ia_agent.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")

    print("Agente con memoria creado (Supervisor de Proyecto)")
    print(f"Archivo: {output_path.resolve()}")


if __name__ == "__main__":
    main()

