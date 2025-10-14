"""
Sistema de plantillas para generar código de agentes AI.

Este módulo contiene las plantillas que generan código Python funcional
para diferentes tipos de agentes usando el framework Agno.
"""

from typing import Dict, List


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
            'duckduckgo': 'from agno.tools.duckduckgo import DuckDuckGoTools',
            'yfinance': 'from agno.tools.yfinance import YFinanceTools',
            'reasoning': 'from agno.tools.reasoning import ReasoningTools',
            'python': 'from agno.tools.python import PythonTools',
            'file': 'from agno.tools.file import FileTools',
            'web': 'from agno.tools.duckduckgo import DuckDuckGoTools',
            'search': 'from agno.tools.duckduckgo import DuckDuckGoTools',
            'finance': 'from agno.tools.yfinance import YFinanceTools',
            'stock': 'from agno.tools.yfinance import YFinanceTools',
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

        if 'duckduckgo' in tool_lower or 'web' in tool_lower or 'search' in tool_lower:
            return 'DuckDuckGoTools()'
        elif 'yfinance' in tool_lower or 'finance' in tool_lower or 'stock' in tool_lower:
            return 'YFinanceTools(stock_price=True, company_info=True)'
        elif 'reasoning' in tool_lower:
            return 'ReasoningTools(add_instructions=True)'
        elif 'python' in tool_lower:
            return 'PythonTools()'
        elif 'file' in tool_lower:
            return 'FileTools()'
        else:
            return f"# Initialize {tool_name} here"

    @staticmethod
    def _build_tools_code(herramientas: List[str]) -> tuple:
        """
        Construye los imports y la lista de herramientas.

        Args:
            herramientas: Lista de nombres de herramientas

        Returns:
            Tupla con (imports, tools_list)
        """
        if not herramientas:
            return "", "[]"

        imports = set()
        tools_init = []

        for tool in herramientas:
            import_line = AgentTemplate._get_tool_import(tool)
            if not import_line.startswith("#"):
                imports.add(import_line)
                tools_init.append(AgentTemplate._generate_tools_init(tool))

        imports_str = "\n".join(sorted(imports))
        tools_str = "[" + ", ".join(tools_init) + "]"

        return imports_str, tools_str

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
        nombre = spec.get('nombre', 'Mi Agente')
        rol = spec.get('rol', 'Asistente general')
        modelo = spec.get('modelo', 'deepseek-chat')
        herramientas = spec.get('herramientas', [])
        instrucciones = spec.get('instrucciones', [])
        ejemplo = spec.get('ejemplo_uso', '¿Cómo puedes ayudarme?')

        # Construir imports de modelo y herramientas
        model_import = AgentTemplate._get_model_import(modelo)
        model_init = AgentTemplate._get_model_init(modelo)
        tools_imports, tools_init = AgentTemplate._build_tools_code(herramientas)

        # Construir lista de instrucciones
        if not instrucciones:
            instrucciones = [f"Eres un {rol}", "Sé útil y conciso", "Responde de forma clara"]

        instrucciones_str = ",\n        ".join([f'"{instr}"' for instr in instrucciones])

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
        tools={tools_init},
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
        nombre = spec.get('nombre', 'Mi Agente')
        rol = spec.get('rol', 'Asistente general')
        modelo = spec.get('modelo', 'deepseek-chat')
        herramientas = spec.get('herramientas', [])
        instrucciones = spec.get('instrucciones', [])
        ejemplo = spec.get('ejemplo_uso', '¿Cómo puedes ayudarme?')

        # Construir imports
        model_import = AgentTemplate._get_model_import(modelo)
        model_init = AgentTemplate._get_model_init(modelo)
        tools_imports, tools_init = AgentTemplate._build_tools_code(herramientas)

        # Instrucciones
        if not instrucciones:
            instrucciones = [f"Eres un {rol}", "Recuerda conversaciones previas", "Sé útil y contextual"]

        instrucciones_str = ",\n        ".join([f'"{instr}"' for instr in instrucciones])

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
        tools={tools_init},
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
        """
        Genera un equipo de agentes colaborativos (Nivel 4).

        Args:
            spec: Especificación del equipo con campos adicionales:
                - miembros_equipo: List[Dict] con {nombre, rol, herramientas}

        Returns:
            Código Python completo como string
        """
        nombre = spec.get('nombre', 'Mi Equipo')
        rol = spec.get('rol', 'Equipo de asistentes')
        modelo = spec.get('modelo', 'deepseek-chat')
        miembros = spec.get('miembros_equipo', [])
        instrucciones = spec.get('instrucciones', [])
        ejemplo = spec.get('ejemplo_uso', '¿Qué puede hacer este equipo?')

        # Imports del modelo
        model_import = AgentTemplate._get_model_import(modelo)
        model_init = AgentTemplate._get_model_init(modelo)

        # Si no hay miembros definidos, crear equipo genérico
        if not miembros:
            miembros = [
                {"nombre": "Researcher", "rol": "Buscar información", "herramientas": ["duckduckgo"]},
                {"nombre": "Analyzer", "rol": "Analizar datos", "herramientas": ["reasoning"]},
                {"nombre": "Writer", "rol": "Escribir respuestas", "herramientas": []},
            ]

        # Construir código de miembros
        all_tools_imports = set()
        members_code = []

        for idx, miembro in enumerate(miembros):
            m_nombre = miembro.get('nombre', f'Member{idx+1}')
            m_rol = miembro.get('rol', 'Miembro del equipo')
            m_herramientas = miembro.get('herramientas', [])

            tools_imports, tools_init = AgentTemplate._build_tools_code(m_herramientas)

            if tools_imports:
                for line in tools_imports.split('\n'):
                    if line.strip():
                        all_tools_imports.add(line)

            members_code.append(f'''
    # Miembro: {m_nombre}
    {m_nombre.lower().replace(' ', '_')} = Agent(
        name="{m_nombre}",
        role="{m_rol}",
        model={model_init},
        tools={tools_init},
    )''')

        tools_imports_str = "\n".join(sorted(all_tools_imports))
        members_str = "\n".join(members_code)

        # Instrucciones del equipo
        if not instrucciones:
            instrucciones = ["Colaboren efectivamente", "Dividan el trabajo según especialidades", "Combinen sus hallazgos"]

        instrucciones_str = ",\n        ".join([f'"{instr}"' for instr in instrucciones])

        # Generar código
        code = f'''"""
{nombre} - Equipo de Agentes AI colaborativos.

Rol: {rol}
Miembros: {len(miembros)}
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
{model_import}
{tools_imports_str}

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal para ejecutar el equipo de agentes."""

    # Crear miembros del equipo
{members_str}

    # Crear el equipo
    team = Team(
        name="{nombre}",
        members=[{', '.join([m.get('nombre', f'member{i}').lower().replace(' ', '_') for i, m in enumerate(miembros)])}],
        model={model_init},
        instructions=[
        {instrucciones_str}
        ],
        markdown=True,
    )

    # Ejemplo de uso
    print("\\n🤖 {nombre} está listo\\n")
    print("Miembros del equipo:")
{chr(10).join([f'    print("  - {m.get("nombre", f"Member{i+1}")}: {m.get("rol", "Miembro del equipo")}")' for i, m in enumerate(miembros)])}
    print("\\nEjemplo de tarea: {ejemplo}\\n")

    # Ejecutar con el ejemplo
    team.print_response("{ejemplo}", stream=True)

    print("\\n")
    print("El equipo colabora automáticamente para completar tareas complejas.")


if __name__ == "__main__":
    main()
'''

        return code
