"""
Meta-Agente Generador de Agentes AI.

Este módulo contiene la lógica principal para analizar solicitudes de usuarios,
crear planes estructurados y generar código de agentes usando el framework Agno.
"""

import json
import os
import re
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from rich.console import Console
from agno.agent import Agent
from agno.models.deepseek import DeepSeek

console = Console()


class AgentPlan(BaseModel):
    """
    Modelo de datos para el plan de un agente.

    Attributes:
        nombre: Nombre del agente a crear
        rol: Descripción del rol que desempeña
        modelo: Modelo LLM a utilizar (deepseek, claude, gpt-4, gemini)
        nivel: Nivel de complejidad (1-5)
        herramientas: Lista de herramientas/tools a incluir
        instrucciones: Instrucciones específicas para el agente
        necesita_memoria: Si requiere persistencia de conversaciones
        es_equipo: Si es un equipo de agentes colaborando
        miembros_equipo: Lista de miembros si es equipo
        ejemplo_uso: Ejemplo de cómo usar el agente
    """
    nombre: str = Field(description="Nombre del agente")
    rol: str = Field(description="Rol o propósito del agente")
    modelo: str = Field(default="deepseek-chat", description="Modelo LLM a usar")
    nivel: int = Field(default=1, ge=1, le=5, description="Nivel de complejidad 1-5")
    herramientas: List[str] = Field(default_factory=list, description="Lista de herramientas")
    instrucciones: List[str] = Field(default_factory=list, description="Instrucciones específicas")
    necesita_memoria: bool = Field(default=False, description="Si necesita memoria persistente")
    es_equipo: bool = Field(default=False, description="Si es un equipo de agentes")
    miembros_equipo: List[Dict] = Field(default_factory=list, description="Miembros del equipo")
    ejemplo_uso: str = Field(default="", description="Ejemplo de uso del agente")


class MetaAgent:
    """
    Meta-agente que genera otros agentes automáticamente.

    Este agente utiliza dos agentes internos:
    - analyzer_agent: Analiza solicitudes y hace preguntas aclaratorias
    - planner_agent: Crea planes estructurados en formato JSON
    """

    def __init__(self):
        """Inicializa el meta-agente con sus agentes internos."""
        self.analysis_model = DeepSeek(id="deepseek-chat")
        self.planning_model = DeepSeek(id="deepseek-reasoner")

        # Agente para analizar solicitudes
        self.analyzer_agent = Agent(
            name="Analyzer Agent",
            role="Analizar solicitudes de usuarios y hacer preguntas aclaratorias",
            model=self.analysis_model,
            instructions=[
                "Analiza la solicitud del usuario para crear un agente AI",
                "Identifica qué información falta para crear un agente completo",
                "Haz preguntas específicas y contextuales",
                "Si tienes toda la información necesaria, responde exactamente: INFO_COMPLETA",
                "Sé conciso y amigable en tus preguntas"
            ],
            markdown=True,
        )

        # Agente para crear planes estructurados
        self.planner_agent = Agent(
            name="Planner Agent",
            role="Crear planes estructurados para agentes AI",
            model=self.planning_model,
            instructions=[
                "Crea un plan detallado en formato JSON",
                "Usa el esquema AgentPlan proporcionado",
                "Infiere información razonable si no está explícita",
                "Sé específico en rol, instrucciones y herramientas",
                "Retorna SOLO el JSON, sin texto adicional"
            ],
            markdown=True,
        )

    def analyze_request(self, user_request: str, conversation_history: str = "") -> str:
        """
        Analiza la solicitud del usuario y determina qué información falta.

        Args:
            user_request: Solicitud actual del usuario
            conversation_history: Historial de la conversación previa

        Returns:
            Preguntas aclaratorias o "INFO_COMPLETA" si tiene todo
        """
        prompt = f"""
Conversación hasta ahora:
{conversation_history}

Solicitud actual del usuario:
{user_request}

Analiza esta solicitud para crear un agente AI. Necesitas saber:
1. ¿Qué debe hacer el agente? (propósito/rol)
2. ¿Qué herramientas necesita? (búsqueda web, finanzas, archivos, etc.)
3. ¿Necesita memoria de conversaciones previas?
4. ¿Es un agente individual o un equipo?
5. ¿Hay instrucciones especiales o restricciones?

Si ya tienes TODA esta información de forma clara, responde exactamente: INFO_COMPLETA

Si falta información, haz 1-2 preguntas específicas para clarificar.
Sugiere opciones concretas cuando sea posible.

Ejemplo de buena pregunta:
"¿Qué herramientas necesita el agente?
a) Búsqueda web (noticias, información general)
b) Datos financieros (acciones, mercados)
c) Análisis de archivos
d) Otra (especifica)"
"""

        response = self.analyzer_agent.run(prompt)
        return response.content

    def create_plan(self, conversation: str) -> AgentPlan:
        """
        Crea un plan estructurado basado en la conversación completa.

        Args:
            conversation: Toda la conversación con el usuario

        Returns:
            AgentPlan estructurado y validado

        Raises:
            ValueError: Si no puede parsear o validar el plan
        """
        # Schema del modelo para el prompt
        schema = AgentPlan.model_json_schema()

        prompt = f"""
Basándote en esta conversación con el usuario, crea un plan completo para el agente:

{conversation}

Retorna un JSON que siga este esquema exacto:
{json.dumps(schema, indent=2)}

Reglas importantes:
- nombre: Nombre descriptivo del agente (ej: "Buscador de Noticias Tech")
- rol: Descripción clara de su función
- modelo: Usa "deepseek-chat" por defecto (o "claude-sonnet-4", "gpt-4o", "gemini-2.0-flash-exp")
- nivel: 1=básico, 2=con conocimiento, 3=con memoria, 4=equipo, 5=workflow
- herramientas: Lista con nombres como ["duckduckgo", "yfinance", "reasoning"]
- instrucciones: Lista de instrucciones específicas
- necesita_memoria: true si debe recordar conversaciones
- es_equipo: true si es un equipo de agentes
- ejemplo_uso: Ejemplo de pregunta/tarea para el agente

Herramientas disponibles:
- duckduckgo: Búsqueda web
- yfinance: Datos financieros
- reasoning: Razonamiento complejo
- python: Ejecutar código Python
- file: Manipular archivos

Retorna SOLO el JSON, sin markdown, sin explicaciones adicionales.
"""

        response = self.planner_agent.run(prompt)
        content = response.content

        # Limpiar contenido si viene con markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        # Intentar extraer JSON con regex si es necesario
        content = content.strip()
        if not content.startswith("{"):
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()

        try:
            plan_dict = json.loads(content)
            plan = AgentPlan(**plan_dict)
            return plan
        except json.JSONDecodeError as e:
            console.print(f"[red]Error al parsear JSON:[/red]")
            console.print(f"[yellow]Contenido recibido:[/yellow]\n{content}")
            raise ValueError(f"No se pudo parsear el plan como JSON: {e}")
        except Exception as e:
            console.print(f"[red]Error al validar el plan:[/red] {e}")
            raise ValueError(f"Plan inválido: {e}")

    def generate_code(self, plan: AgentPlan) -> str:
        """
        Genera el código Python del agente basado en el plan.

        Args:
            plan: Plan estructurado del agente

        Returns:
            Código Python completo como string
        """
        from src.infrastructure.templates.agent_templates import AgentTemplate

        # Ajustar modelo sugerido según el tipo de agente
        if plan.es_equipo and plan.modelo == "deepseek-chat":
            plan.modelo = "deepseek-reasoner"

        if plan.es_equipo:
            return AgentTemplate.generate_agent_team(plan.model_dump())
        elif plan.necesita_memoria or plan.nivel >= 3:
            return AgentTemplate.generate_agent_with_memory(plan.model_dump())
        else:
            return AgentTemplate.generate_basic_agent(plan.model_dump())

    def interactive_creation(self):
        """
        Proceso interactivo completo para crear un agente.

        Guía al usuario a través de:
        1. Solicitud inicial
        2. Preguntas aclaratorias (hasta 5 iteraciones)
        3. Creación del plan
        4. Confirmación
        5. Generación y guardado del código
        """
        console.print("\n[bold cyan]🤖 Meta-Agente Generador de Agentes AI[/bold cyan]")
        console.print("[dim]Voy a ayudarte a crear un agente personalizado[/dim]\n")

        # Paso 1: Solicitud inicial
        console.print("[bold]¿Qué tipo de agente necesitas?[/bold]")
        console.print("[dim]Ejemplo: 'Un agente que busque noticias de tecnología'[/dim]")
        user_input = input("\n> ").strip()

        if not user_input:
            console.print("[red]No puedo crear un agente sin una descripción.[/red]")
            return

        conversation = f"Usuario: {user_input}"

        # Paso 2: Loop de preguntas aclaratorias
        max_iterations = 5
        for iteration in range(max_iterations):
            console.print(f"\n[dim]Analizando... ({iteration + 1}/{max_iterations})[/dim]")

            analysis = self.analyze_request(user_input, conversation)

            if "INFO_COMPLETA" in analysis:
                console.print("\n[green]✓ Tengo toda la información necesaria[/green]")
                break

            console.print(f"\n[bold cyan]Meta-Agente:[/bold cyan]")
            console.print(analysis)

            user_response = input("\n> ").strip()
            if not user_response:
                console.print("[yellow]Continuando con la información actual...[/yellow]")
                break

            conversation += f"\n\nMeta-Agente: {analysis}"
            conversation += f"\nUsuario: {user_response}"
            user_input = user_response

        # Paso 3: Crear plan
        console.print("\n[bold]Creando plan del agente...[/bold]")

        try:
            plan = self.create_plan(conversation)
        except Exception as e:
            console.print(f"[red]Error al crear el plan: {e}[/red]")
            return

        # Paso 4: Mostrar plan y confirmar
        console.print("\n[bold green]📋 Plan del Agente:[/bold green]")
        console.print(f"[cyan]Nombre:[/cyan] {plan.nombre}")
        console.print(f"[cyan]Rol:[/cyan] {plan.rol}")
        console.print(f"[cyan]Modelo:[/cyan] {plan.modelo}")
        console.print(f"[cyan]Nivel:[/cyan] {plan.nivel}")
        console.print(f"[cyan]Herramientas:[/cyan] {', '.join(plan.herramientas) if plan.herramientas else 'Ninguna'}")
        console.print(f"[cyan]Memoria:[/cyan] {'Sí' if plan.necesita_memoria else 'No'}")
        console.print(f"[cyan]Tipo:[/cyan] {'Equipo' if plan.es_equipo else 'Individual'}")

        console.print("\n[bold]¿Proceder con la generación? (s/n):[/bold]")
        confirm = input("> ").strip().lower()

        if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
            console.print("[yellow]Generación cancelada.[/yellow]")
            return

        # Paso 5: Generar código
        console.print("\n[bold]Generando código...[/bold]")

        try:
            code = self.generate_code(plan)
        except Exception as e:
            console.print(f"[red]Error al generar código: {e}[/red]")
            return

        # Paso 6: Guardar archivo
        filename = f"{plan.nombre.lower().replace(' ', '_')}_agent.py"
        output_dir = os.path.join(os.getcwd(), "generated", "agents")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        console.print(f"\n[bold green]✓ Agente generado exitosamente:[/bold green] {filepath}")
        console.print("\n[bold]Para usar tu agente:[/bold]")
        console.print(f"1. Asegúrate de tener las dependencias: pip install -r requirements.txt")
        console.print(f"2. Configura tu .env con las API keys necesarias")
        console.print(f"3. Ejecuta: python {filepath}")
