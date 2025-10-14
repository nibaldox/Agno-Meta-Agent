"""
Punto de entrada CLI para el Meta-Agente Generador.

Este script valida el entorno y ejecuta el flujo interactivo
para crear agentes AI personalizados.
"""

import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from src.application.services.meta_agent import MetaAgent

console = Console()


def check_environment() -> bool:
    """
    Verifica que el entorno esté configurado correctamente.

    Returns:
        True si el entorno es válido, False en caso contrario
    """
    # Cargar variables de entorno
    load_dotenv()

    # Verificar API key de Anthropic (mínimo requerido)
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        console.print("[bold red]❌ Error: ANTHROPIC_API_KEY no configurada[/bold red]")
        console.print("\n[yellow]Para configurar:[/yellow]")
        console.print("1. Copia .env.example a .env")
        console.print("2. Edita .env y añade tu API key de Anthropic")
        console.print("3. Obtén tu API key en: https://console.anthropic.com/\n")
        return False

    return True


def show_welcome():
    """Muestra el mensaje de bienvenida."""
    console.print("\n" + "="*60)
    console.print("[bold cyan]🤖 Meta-Agente Generador de Agentes AI[/bold cyan]", justify="center")
    console.print("="*60 + "\n")

    console.print("[dim]Este sistema te ayuda a crear agentes AI personalizados\n"
                  "usando el framework Agno y modelos DeepSeek.[/dim]\n")


def main():
    """Función principal del programa."""

    show_welcome()

    # Verificar configuración
    if not check_environment():
        console.print("[red]Por favor configura el entorno antes de continuar.[/red]")
        sys.exit(1)

    console.print("[green]✓ Entorno configurado correctamente[/green]\n")

    try:
        # Crear instancia del meta-agente
        meta_agent = MetaAgent()

        # Ejecutar flujo interactivo
        meta_agent.interactive_creation()

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Proceso interrumpido por el usuario.[/yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(f"\n[bold red]Error inesperado:[/bold red] {e}")
        console.print("[dim]Si el problema persiste, revisa los logs o reporta el issue.[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()
