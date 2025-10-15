"""
Sistema de plantillas para generar código de agentes AI.

Este módulo contiene las plantillas que generan código Python funcional
para diferentes tipos de agentes usando el framework Agno.
"""

from typing import Dict, List, Tuple


class AgentTemplate:
    """
    Generador de código para agentes AI.

    Proporciona métodos estáticos para generar diferentes tipos de agentes:
    - Agentes básicos con herramientas
    - Agentes con memoria y storage
    - Equipos de agentes colaborativos
    """

    @staticmethod
    def _get_model_import(modelo: str) -> str:
        """
        Retorna el import statement para el modelo especificado.

        Args:
            modelo: Nombre del modelo (claude, gpt-4, gemini)

        Returns:
            String con el import del modelo
        """
        modelo_lower = modelo.lower()

        if "deepseek" in modelo_lower:
            return "from agno.models.deepseek import DeepSeek"
        elif "claude" in modelo_lower or "sonnet" in modelo_lower:
            return "from agno.models.anthropic import Claude"
        elif "gpt" in modelo_lower or "openai" in modelo_lower:
            return "from agno.models.openai import OpenAIChat"
        elif "gemini" in modelo_lower or "google" in modelo_lower:
            return "from agno.models.google import Gemini"
        else:
            # Default a Claude
            return "from agno.models.anthropic import Claude"

    @staticmethod
    def _get_model_init(modelo: str) -> str:
        """
        Retorna el código de inicialización del modelo.

        Args:
            modelo: Nombre del modelo

        Returns:
            String con la inicialización del modelo
        """
        modelo_lower = modelo.lower()

        if "deepseek" in modelo_lower:
            model_id = modelo if "deepseek" in modelo_lower else "deepseek-chat"
            return f'DeepSeek(id="{model_id}")'
        elif "claude" in modelo_lower or "sonnet" in modelo_lower:
            model_id = modelo if "claude-" in modelo else "claude-sonnet-4-20250514"
            return f'Claude(id="{model_id}")'
        elif "gpt" in modelo_lower or "openai" in modelo_lower:
            model_id = modelo if "gpt-" in modelo else "gpt-4o"
            return f'OpenAIChat(id="{model_id}")'
        elif "gemini" in modelo_lower or "google" in modelo_lower:
            model_id = modelo if "gemini-" in modelo else "gemini-2.0-flash-exp"
            return f'Gemini(id="{model_id}")'
        else:
            return 'DeepSeek(id="deepseek-chat")'

    @staticmethod
    def _get_tool_import(tool_name: str) -> str:
        """
        Retorna el import statement para una herramienta.

        Args:
            tool_name: Nombre de la herramienta

        Returns:
            String con el import de la herramienta
        """
        tool_map = {
            "duckduckgo": "from agno.tools.duckduckgo import DuckDuckGoTools",
            "serper": "from agno.tools.serper import SerperTools",
            "yfinance": "from agno.tools.yfinance import YFinanceTools",
            "reasoning": "from agno.tools.reasoning import ReasoningTools",
            "python": "from agno.tools.python import PythonTools",
            "file": "from agno.tools.file import FileTools",
            "web": "from agno.tools.duckduckgo import DuckDuckGoTools",
            "search": "from agno.tools.duckduckgo import DuckDuckGoTools",
            "finance": "from agno.tools.yfinance import YFinanceTools",
            "stock": "from agno.tools.yfinance import YFinanceTools",
        }

        tool_lower = tool_name.lower()
        return tool_map.get(tool_lower, f"# Tool '{tool_name}' not found")

    @staticmethod
    def _generate_tools_init(tool_name: str) -> str:
        """
        Retorna el código de inicialización de una herramienta.

        Args:
            tool_name: Nombre de la herramienta

        Returns:
            String con la inicialización de la herramienta
        """
        tool_lower = tool_name.lower()

        if "duckduckgo" in tool_lower or "web" in tool_lower or "search" in tool_lower:
            return "DuckDuckGoTools()"
        elif "serper" in tool_lower:
            return 'SerperTools(api_key=os.getenv("SERPER_API_KEY"))'
        elif (
            "yfinance" in tool_lower or "finance" in tool_lower or "stock" in tool_lower
        ):
            return "YFinanceTools(stock_price=True, company_info=True)"
        elif "reasoning" in tool_lower:
            return "ReasoningTools(add_instructions=True)"
        elif "python" in tool_lower:
            return "PythonTools()"
        elif "file" in tool_lower:
            return "FileTools()"
        else:
            return f"# Initialize {tool_name} here"

    @staticmethod
    def _build_tools_code(herramientas: List[str]) -> Tuple[str, str, List[str]]:
        """
        Construye los imports y la lista de herramientas.

        Args:
            herramientas: Lista de nombres de herramientas

        Returns:
            Tupla con (imports, tools_list, comentarios_placeholder)
        """
        if not herramientas:
            return "", "[]", []

        imports = set()
        tools_init = []
        has_valid_tools = False
        placeholders: List[str] = []

        needs_serper_fallback = False
        serper_requested = False

        for tool in herramientas:
            import_line = AgentTemplate._get_tool_import(tool)
            tool_init = AgentTemplate._generate_tools_init(tool)

            if import_line.startswith("#"):
                # Mantener placeholder en lista de herramientas
                placeholders.append(tool_init)
                continue

            imports.add(import_line)
            tools_init.append(tool_init)
            has_valid_tools = True

            tool_lower = tool.lower()
            if any(keyword in tool_lower for keyword in ("duckduckgo", "web", "search")):
                needs_serper_fallback = True
            if "serper" in tool_lower:
                serper_requested = True

        if needs_serper_fallback and not serper_requested:
            imports.add("from agno.tools.serper import SerperTools")
            tools_init.append('SerperTools(api_key=os.getenv("SERPER_API_KEY"))')
            has_valid_tools = True

        imports_str = "\n".join(sorted(imports))

        if has_valid_tools:
            tools_str = "[" + ", ".join(tools_init) + "]"
        else:
            tools_str = "[]"

        return imports_str, tools_str, placeholders

    @staticmethod
    def generate_basic_agent(spec: Dict) -> str:
        """
        Genera un agente básico (Nivel 1).

        Args:
            spec: Especificación del agente con campos:
                - nombre: str
                - rol: str
                - modelo: str
                - herramientas: List[str]
                - instrucciones: List[str]
                - ejemplo_uso: str

        Returns:
            Código Python completo como string
        """
        nombre = spec.get("nombre", "Mi Agente")
        rol = spec.get("rol", "Asistente general")
        modelo = spec.get("modelo", "deepseek-chat")
        herramientas = spec.get("herramientas", [])
        instrucciones = spec.get("instrucciones", [])
        ejemplo = spec.get("ejemplo_uso", "¿Cómo puedes ayudarme?")

        # Construir imports de modelo y herramientas
        model_import = AgentTemplate._get_model_import(modelo)
        model_init = AgentTemplate._get_model_init(modelo)
        tools_imports, tools_init, tools_placeholders = AgentTemplate._build_tools_code(
            herramientas
        )

        # Construir lista de instrucciones
        if not instrucciones:
            instrucciones = [
                f"Eres un {rol}",
                "Sé útil y conciso",
                "Responde de forma clara",
            ]

        instrucciones_str = ",\n        ".join(
            [f'"{instr}"' for instr in instrucciones]
        )

        tools_placeholder_comment = ""
        if tools_placeholders:
            placeholder_lines = "\n        ".join(tools_placeholders)
            tools_placeholder_comment = f"\n        {placeholder_lines}"

        # Generar código
        code = f'''"""
{nombre} - Agente AI generado automáticamente.

Rol: {rol}
Herramientas: {', '.join(herramientas) if herramientas else 'Ninguna'}
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
{model_import}
{tools_imports}

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el agente."""

    # Crear el agente
    agent = Agent(
        name="{nombre}",
        role="{rol}",
        model={model_init},
        tools={tools_init},{tools_placeholder_comment}
        instructions=[
        {instrucciones_str}
        ],
        markdown=True,
    )

    # Ejemplo de uso
    print("\\n🤖 {nombre} está listo\\n")
    print("Ejemplo de pregunta: {ejemplo}\\n")

    # Ejecutar con el ejemplo
    agent.print_response("{ejemplo}", stream=True)

    print("\\n")
    print("Para usar interactivamente, modifica este archivo y usa agent.print_response(tu_pregunta)")


if __name__ == "__main__":
    main()
'''

        return code

    @staticmethod
    def generate_agent_with_memory(spec: Dict) -> str:
        """
        Genera un agente con memoria persistente (Nivel 3).

        Args:
            spec: Especificación del agente (mismos campos que generate_basic_agent)

        Returns:
            Código Python completo como string
        """
        nombre = spec.get("nombre", "Mi Agente")
        rol = spec.get("rol", "Asistente general")
        modelo = spec.get("modelo", "deepseek-chat")
        herramientas = spec.get("herramientas", [])
        instrucciones = spec.get("instrucciones", [])
        ejemplo = spec.get("ejemplo_uso", "¿Cómo puedes ayudarme?")

        # Construir imports
        model_import = AgentTemplate._get_model_import(modelo)
        model_init = AgentTemplate._get_model_init(modelo)
        tools_imports, tools_init, tools_placeholders = AgentTemplate._build_tools_code(
            herramientas
        )

        # Instrucciones
        if not instrucciones:
            instrucciones = [
                f"Eres un {rol}",
                "Recuerda conversaciones previas",
                "Sé útil y contextual",
            ]

        instrucciones_str = ",\n        ".join(
            [f'"{instr}"' for instr in instrucciones]
        )

        tools_placeholder_comment = ""
        if tools_placeholders:
            placeholder_lines = "\n        ".join(tools_placeholders)
            tools_placeholder_comment = f"\n        {placeholder_lines}"

        # Generar código
        code = f'''"""
{nombre} - Agente AI con memoria persistente.

Rol: {rol}
Herramientas: {', '.join(herramientas) if herramientas else 'Ninguna'}
Memoria: Activada (SQLite)
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
{model_import}
{tools_imports}

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el agente con memoria."""

    # Configurar storage
    db = SqliteDb(db_file="agents_memory.sqlite")

    # Crear el agente
    agent = Agent(
        name="{nombre}",
        role="{rol}",
        model={model_init},
        tools={tools_init},{tools_placeholder_comment}
        instructions=[
        {instrucciones_str}
        ],
        db=db,
        markdown=True,
        enable_user_memories=True,
        enable_session_summary=True,
    )

    # Ejemplo de uso
    print("\\n🤖 {nombre} está listo (con memoria)\\n")
    print("Ejemplo de pregunta: {ejemplo}\\n")

    # Ejecutar con el ejemplo
    agent.print_response("{ejemplo}", stream=True)

    print("\\n")
    print("💾 Las conversaciones se guardan en: agents_memory.sqlite")
    print("El agente recordará contexto de sesiones anteriores.")


if __name__ == "__main__":
    main()
'''

        return code

    @staticmethod
    def generate_agent_team(spec: Dict) -> str:
        """Genera un equipo colaborativo (Nivel 4) a partir de la especificación."""

        nombre = spec.get("nombre", "Mi Equipo")
        rol = spec.get("rol", "Equipo de asistentes")
        modelo = spec.get("modelo", "deepseek-chat")
        miembros = spec.get("miembros_equipo", [])
        instrucciones = spec.get("instrucciones", [])
        ejemplo = spec.get("ejemplo_uso", "¿Qué puede hacer este equipo?")

        model_import = AgentTemplate._get_model_import(modelo)
        model_init = AgentTemplate._get_model_init(modelo)

        if not miembros:
            miembros = [
                {
                    "nombre": "Researcher",
                    "rol": "Buscar información",
                    "herramientas": ["duckduckgo"],
                },
                {
                    "nombre": "Analyzer",
                    "rol": "Analizar datos",
                    "herramientas": ["reasoning"],
                },
                {
                    "nombre": "Writer",
                    "rol": "Escribir respuestas",
                    "herramientas": [],
                },
            ]

        extra_imports: set[str] = set()
        member_blocks: List[str] = []
        member_vars: List[str] = []
        member_info_pairs: List[Tuple[str, str]] = []

        for idx, member in enumerate(miembros):
            member_name = member.get("nombre", f"Member{idx + 1}")
            member_role = member.get("rol", "Miembro del equipo")
            member_tools = member.get("herramientas", [])

            imports_line, tools_init, placeholders = AgentTemplate._build_tools_code(
                member_tools
            )

            if imports_line:
                extra_imports.update(line for line in imports_line.split("\n") if line)

            placeholder_comment = ""
            if placeholders:
                placeholder_comment = "\n        " + "\n        ".join(placeholders)

            member_var = f"miembro_{idx}"
            member_vars.append(member_var)
            member_blocks.append(
                f"""
    # Miembro: {member_name}
    {member_var} = Agent(
        name="{member_name}",
        role="{member_role}",
        model={model_init},
        tools={tools_init},{placeholder_comment}
    )"""
            )
            member_info_pairs.append((member_name, member_role))

        if not member_blocks:
            member_blocks.append(
                """
    # Miembro: Miembro Defecto
    miembro_0 = Agent(
        name="Miembro Defecto",
        role="Rol indefinido",
        model={model_init},
        tools=[],
    )"""
            )
            member_vars = ["miembro_0"]
            member_info_pairs = [("Miembro Defecto", "Rol indefinido")]

        instructions_list = instrucciones or [
            "Colaboren efectivamente",
            "Dividan el trabajo según especialidades",
            "Combinen sus hallazgos",
        ]
        instructions_code = ",\n        ".join(f'"{item}"' for item in instructions_list)

        imports_code = "\n".join(sorted(extra_imports))
        members_code = "\n".join(member_blocks)
        member_vars_code = ", ".join(member_vars)
        member_info_code = ",\n        ".join(
            [
                f'("{name.replace("\"", "\\\"")}", "{role.replace("\"", "\\\"")}")'
                for name, role in member_info_pairs
            ]
        )

        code = f'''"""
{nombre} - Equipo de Agentes AI colaborativos.

Rol: {rol}
Miembros: {len(member_info_pairs)}
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
{model_import}
{imports_code}

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el equipo de agentes."""

    # Crear miembros del equipo
{members_code}

    member_info = [
        {member_info_code}
    ]

    team = Team(
        name="{nombre}",
        members=[{member_vars_code}],
        model={model_init},
        instructions=[
        {instructions_code}
        ],
        markdown=True,
    )

    print("\\n🤖 {nombre} está listo\\n")
    print("Miembros del equipo:")
    for display_name, display_role in member_info:
        print(f"  - {{display_name}}: {{display_role}}")

    print("\\nEjemplo de tarea: {ejemplo}\\n")

    team.print_response("{ejemplo}", stream=True)

    print("\\n")
    print("El equipo colabora automáticamente para completar tareas complejas.")


if __name__ == "__main__":
    main()
'''

        return code
