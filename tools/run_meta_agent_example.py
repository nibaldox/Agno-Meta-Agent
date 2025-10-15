"""Script de ejemplo para probar el Meta-Agente.

Genera un agente sencillo usando `MetaAgent` y guarda el resultado
en `generated/agents/demo_web_research_agent.py`.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.application.services.meta_agent import AgentPlan, MetaAgent


def main() -> None:
    """Genera un agente de ejemplo y lo guarda en disco."""

    plan = AgentPlan(
        nombre="Demo Web Research Agent",
        rol="Buscar noticias recientes sobre inteligencia artificial",
        modelo="deepseek-chat",
        nivel=1,
        herramientas=["duckduckgo"],
        instrucciones=[
            "Saluda al usuario de forma cordial",
            "Usa la herramienta de búsqueda web para obtener la información",
            "Resume la noticia destacando la fecha y la fuente",
        ],
        necesita_memoria=False,
        es_equipo=False,
        miembros_equipo=[],
        ejemplo_uso="¿Qué hay de nuevo en IA hoy?",
    )

    meta_agent = MetaAgent()
    code = meta_agent.generate_code(plan)

    output_path = Path("generated/agents/demo_web_research_agent.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")

    print("Agente generado correctamente")
    print(f"Archivo: {output_path.resolve()}")
    print("Puedes ejecutarlo con: python generated/agents/demo_web_research_agent.py")


if __name__ == "__main__":
    main()

