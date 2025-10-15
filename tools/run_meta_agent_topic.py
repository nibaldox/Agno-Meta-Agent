"""Genera un agente orientado a explorar un tema específico."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.application.services.meta_agent import AgentPlan, MetaAgent


def main() -> None:
    """Genera un agente centrado en investigar un tema concreto."""

    plan = AgentPlan(
        nombre="Explorador de Tendencias IA",
        rol=(
            "Investigar un tema de inteligencia artificial y entregar puntos clave,"
            " incluyendo enlaces relevantes"
        ),
        modelo="deepseek-chat",
        nivel=1,
        herramientas=["duckduckgo", "reasoning"],
        instrucciones=[
            "Pregunta al usuario cuál es el tema específico dentro de la IA",
            "Realiza una búsqueda rápida sobre el tema",
            "Resume tres hallazgos clave con fuente y fecha",
        ],
        necesita_memoria=False,
        es_equipo=False,
        miembros_equipo=[],
        ejemplo_uso="Explora el estado actual del aprendizaje federado",
    )

    meta_agent = MetaAgent()
    code = meta_agent.generate_code(plan)

    output_path = Path("generated/agents/explorador_tendencias_ia_agent.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")

    print("Agente para explorar temas creado con éxito")
    print(f"Archivo: {output_path.resolve()}")


if __name__ == "__main__":
    main()

