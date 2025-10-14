# 🚀 Meta-Agente Generador - Contexto de Proyecto para Cursor

> **INSTRUCCIÓN PARA CURSOR AI:** Este es un proyecto de generación automática de agentes AI. Lee este documento completo antes de hacer modificaciones. Usa los patrones y convenciones aquí descritos.

---

## 📋 QUICK REFERENCE

| Aspecto | Detalle |
|---------|---------|
| **Lenguaje** | Python 3.10+ |
| **Framework Principal** | Agno (AI Agents Framework) |
| **LLM** | Anthropic Claude Sonnet 4 |
| **Validación** | Pydantic v2 |
| **UI** | Rich (Terminal) |
| **Estilo** | PEP 8, Type hints obligatorios |

---

## 🎯 OBJETIVO DEL PROYECTO EN 30 SEGUNDOS

**Meta-agente que genera otros agentes automáticamente.**

```
Usuario: "Necesito un agente que busque noticias"
         ↓
Meta-Agente: Hace preguntas aclaratorias
         ↓
Plan estructurado (JSON)
         ↓
Código Python funcional (Agno)
         ↓
Archivo .py listo para ejecutar
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
meta-agente/
├── meta_agent.py           # ⭐ Orquestador principal (150 líneas)
│   └── MetaAgent           # Clase con 2 agentes internos:
│       ├── analyzer_agent  #    - Analiza solicitudes
│       └── planner_agent   #    - Crea planes
│
├── agent_templates.py      # ⭐ Generador de código (250 líneas)
│   └── AgentTemplate       # Métodos estáticos que generan código:
│       ├── generate_basic_agent()      # Nivel 1
│       ├── generate_agent_with_memory()# Nivel 3
│       └── generate_agent_team()       # Nivel 4
│
├── main.py                 # 🚪 Entrada CLI (50 líneas)
├── requirements.txt        # 📦 Dependencias (6 paquetes)
└── .env                    # 🔑 API keys
```

---

## 🔑 CONCEPTOS CLAVE

### 1. Los 5 Niveles de Agentes

```python
# Nivel 1: Básico + Herramientas
Agent(tools=[DuckDuckGoTools()])

# Nivel 2: + Conocimiento
Agent(tools=[...], knowledge=Knowledge(...))

# Nivel 3: + Memoria
Agent(tools=[...], memory=AgentMemory(), storage=Storage())

# Nivel 4: Equipos
Team(members=[agent1, agent2, agent3])

# Nivel 5: Workflows (futuro)
Workflow(steps=[...])
```

### 2. Flujo del Meta-Agente

```python
# Paso 1: Análisis
conversation = "Usuario: Necesito..."
analysis = analyzer_agent.run(prompt_con_contexto)

# Paso 2: Planificación
plan_json = planner_agent.run(prompt_estructurado)
plan = AgentPlan(**json.loads(plan_json))

# Paso 3: Generación
code = AgentTemplate.generate_basic_agent(spec)

# Paso 4: Guardado
with open(f"{nombre}_agent.py", "w") as f:
    f.write(code)
```

### 3. Sistema de Templates

Las templates son **métodos estáticos que retornan strings de código Python**:

```python
@staticmethod
def generate_basic_agent(spec: Dict) -> str:
    code = f'''
from agno.agent import Agent

agent = Agent(
    name="{spec['nombre']}",
    # ... más config
)
'''
    return code  # String listo para guardar como .py
```

---

## 💻 PATRONES DE CÓDIGO IMPORTANTES

### Pattern 1: Usar Pydantic para Datos Estructurados

```python
# ✅ CORRECTO - Siempre
class AgentPlan(BaseModel):
    nombre: str = Field(description="...")
    nivel: int = Field(description="...")

# ❌ INCORRECTO - Nunca
class AgentPlan:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
```

**Por qué:** Validación automática, serialización JSON, documentación.

### Pattern 2: Código Generado con f-strings

```python
# ✅ CORRECTO
def generate_agent(spec):
    return f'''
from agno.agent import Agent

agent = Agent(
    name="{spec.get('nombre', 'Default')}",
    tools=[{self._tools(spec)}],
)
'''

# ❌ INCORRECTO - No usar concatenación
code = "from agno.agent import Agent\n"
code += "agent = Agent(\n"
# ... difícil de mantener
```

**Por qué:** Legibilidad, mantenibilidad, rendimiento.

### Pattern 3: Mapeo de Configuración a Código

```python
# ✅ CORRECTO - Usar diccionarios de mapeo
TOOL_MAP = {
    'duckduckgo': ('from agno.tools.duckduckgo import DuckDuckGoTools', 'DuckDuckGoTools()'),
    'yfinance': ('from agno.tools.yfinance import YFinanceTools', 'YFinanceTools(...)'),
}

def get_tool_code(tool_name):
    return TOOL_MAP.get(tool_name.lower())

# ❌ INCORRECTO - If-elif gigante
def get_tool_code(tool_name):
    if tool_name == 'duckduckgo':
        return ...
    elif tool_name == 'yfinance':
        return ...
    # ... 20 más líneas
```

**Por qué:** Extensibilidad, DRY principle.

---

## 🛠️ REGLAS DE ORO PARA MODIFICACIONES

### ✅ SIEMPRE:

1. **Mantén la firma pública de funciones**
   ```python
   # Si existe:
   def generate_basic_agent(spec: Dict) -> str:
   # No cambies a:
   def generate_basic_agent(config, options=None) -> List[str]:
   ```

2. **Usa type hints**
   ```python
   def create_plan(conversation: str) -> AgentPlan:  # ✅
   def create_plan(conversation):                     # ❌
   ```

3. **Maneja errores específicamente**
   ```python
   try:
       plan = json.loads(content)
   except json.JSONDecodeError as e:  # ✅ Específico
       logger.error(f"JSON inválido: {content}")
   except Exception:                   # ❌ Muy genérico
   ```

4. **Documenta con docstrings**
   ```python
   def analyze_request(self, user_request: str) -> str:
       """
       Analiza la solicitud del usuario.
       
       Args:
           user_request: Descripción de lo que el usuario quiere
           
       Returns:
           Preguntas aclaratorias o "INFO_COMPLETA"
       """
   ```

### ❌ NUNCA:

1. **Cambiar imports principales sin actualizar requirements.txt**
2. **Hardcodear valores que deberían estar en .env**
3. **Romper compatibilidad con código ya generado**
4. **Ignorar el formato Rich Console en outputs**
5. **Usar print() en lugar de console.print()**

---

## 🎨 CONVENCIONES DE ESTILO

```python
# Naming
class MetaAgent:           # ✅ PascalCase para clases
    def analyze_request:   # ✅ snake_case para funciones
        max_iterations = 5 # ✅ snake_case para variables
        TOOL_MAP = {...}   # ✅ UPPER_SNAKE para constantes

# Imports (orden)
import json               # 1. Standard library
from typing import Dict   # 2. Typing
from pydantic import ...  # 3. Third-party
from meta_agent import... # 4. Local

# Spacing
def function():           # 2 líneas antes de función
    """Docstring."""
    
    x = 1                 # 1 línea entre bloques lógicos
    y = 2
    
    if x:                 # 1 línea antes de if
        return y

class MyClass:            # 2 líneas antes de clase
    """Class docstring."""
```

---

## 🔍 DEBUGGING RÁPIDO

### Problema: El JSON no se parsea

```python
# En meta_agent.py línea ~120
content = response.content
print(f"DEBUG: Contenido recibido:\n{content}")  # Añade esto

# Limpieza actual:
if "```json" in content:
    content = content.split("```json")[1].split("```")[0]

# Si sigue fallando, intenta:
import re
json_match = re.search(r'\{.*\}', content, re.DOTALL)
if json_match:
    content = json_match.group()
```

### Problema: Herramienta no encontrada

```python
# En agent_templates.py
# Revisa TOOL_MAP en _get_tool_import()
# Añade entrada:
TOOL_MAP = {
    'nueva_herramienta': 'from agno.tools.nueva import NuevaTools',
    # ...
}
```

### Problema: Rich no muestra colores

```python
# En cualquier archivo con Console
from rich.console import Console
console = Console(force_terminal=True)  # Fuerza colores
```

---

## 📚 REFERENCIAS RÁPIDAS

### Agno Framework

```python
# Crear agente básico
from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    name="Mi Agente",
    role="Lo que hace",
    model=Claude(id="claude-sonnet-4-20250514"),
    tools=[...],
    instructions=["lista", "de", "instrucciones"],
    markdown=True,
)

# Ejecutar
response = agent.run("Pregunta del usuario")
print(response.content)

# O streaming
agent.print_response("Pregunta", stream=True)
```

### Herramientas Disponibles

```python
# Web Search
from agno.tools.duckduckgo import DuckDuckGoTools
tools = [DuckDuckGoTools()]

# Finanzas
from agno.tools.yfinance import YFinanceTools
tools = [YFinanceTools(stock_price=True)]

# Razonamiento
from agno.tools.reasoning import ReasoningTools
tools = [ReasoningTools(add_instructions=True)]

# Python REPL
from agno.tools.python import PythonTools
tools = [PythonTools()]
```

### Pydantic Basics

```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str = Field(description="El nombre")
    age: int = Field(default=0, ge=0)  # >= 0
    tags: List[str] = Field(default_factory=list)

# Crear
m = MyModel(name="Juan", age=30)

# Serializar
json_str = m.model_dump_json()

# Parsear
m2 = MyModel.model_validate_json(json_str)
```

---

## 🎯 TAREAS COMUNES Y CÓMO HACERLAS

### Añadir Nueva Herramienta

1. Ve a `agent_templates.py`
2. En `_get_tool_import()`: Añade entrada al diccionario
3. En `_generate_tools_init()`: Añade caso en el if
4. Test: Genera agente con esa herramienta

### Cambiar Prompt del Analyzer

1. Ve a `meta_agent.py` línea ~40
2. Modifica el f-string en `analyze_request()`
3. Test: Corre main.py y verifica preguntas

### Crear Nuevo Tipo de Template

1. Ve a `agent_templates.py`
2. Añade método `generate_TIPO_agent(spec: Dict) -> str:`
3. Sigue patrón de `generate_basic_agent()`
4. Actualiza `generate_code()` en meta_agent.py para usarlo

### Mejorar UI

1. Ve a `meta_agent.py` → `interactive_creation()`
2. Usa componentes de Rich: `Table`, `Syntax`, `Progress`
3. Referencia: https://rich.readthedocs.io

---

## ⚠️ COSAS QUE ROMPERÍAN EL SISTEMA

1. **Cambiar el nombre de AgentPlan** → Muchos lugares lo usan
2. **Cambiar firma de generate_*_agent()** → API pública
3. **Cambiar formato del JSON del planner** → Parsing fallaría
4. **Remover Rich Console** → UI se rompería
5. **Cambiar estructura de spec en templates** → Templates fallarían

Si necesitas hacer cambios grandes, **pregunta primero** o haz **refactor incremental**.

---

## 🚀 CÓMO EXTENDER EL SISTEMA

### Añadir Nivel 5 (Workflows)

```python
# 1. Crear template en agent_templates.py
@staticmethod
def generate_workflow(spec: Dict) -> str:
    return f'''
from agno.workflow import Workflow
# ... código del workflow
'''

# 2. Actualizar AgentPlan en meta_agent.py
class AgentPlan(BaseModel):
    # ... campos existentes
    es_workflow: bool = False
    workflow_steps: List[Dict] = Field(default_factory=list)

# 3. Actualizar generate_code() en meta_agent.py
def generate_code(self, plan: AgentPlan) -> str:
    if plan.es_workflow:
        return AgentTemplate.generate_workflow(spec)
    # ... resto del código
```

### Añadir API REST

```python
# Crear api.py
from fastapi import FastAPI
from meta_agent import MetaAgent, AgentPlan

app = FastAPI()
meta = MetaAgent()

@app.post("/generate")
def generate_agent(plan: AgentPlan):
    code = meta.generate_code(plan)
    return {"code": code, "filename": f"{plan.nombre}_agent.py"}

# Ejecutar: uvicorn api:app --reload
```

---

## 💬 COMUNICARSE CON CURSOR AI

### Ejemplos de Buenos Prompts

```
✅ "En agent_templates.py línea 150, refactoriza _get_tool_import() 
   para usar un diccionario en lugar de if-elif. Mantén la misma API."

✅ "Añade type hints a todas las funciones en meta_agent.py. 
   Sigue el estilo existente."

✅ "Crea tests unitarios para generate_basic_agent() en 
   agent_templates.py. Usa pytest y cubre casos edge."
```

### Ejemplos de Malos Prompts

```
❌ "Mejora el código"  # Muy vago
❌ "Arregla los bugs"  # ¿Qué bugs?
❌ "Haz esto más rápido"  # Sin contexto
```

### Template de Prompt Efectivo

```
[TAREA]: Descripción clara y específica

[CONTEXTO]: 
- Archivo: nombre.py
- Líneas: X-Y
- Problema/Objetivo: ...

[REQUISITOS]:
1. Requisito específico 1
2. Requisito específico 2

[RESTRICCIONES]:
- No cambiar la API pública
- Mantener compatibilidad con...
```

---

## 📞 AYUDA Y RECURSOS

- **Docs de Agno:** https://docs.agno.com
- **Agno GitHub:** https://github.com/agno-agi/agno
- **Este Proyecto:** Ver .cursorrules y CURSOR_PROMPTS.md

---

**🎓 REGLA FINAL PARA CURSOR AI:**

> Antes de modificar código, pregúntate:
> 1. ¿Entiendo qué hace este código?
> 2. ¿Mi cambio mantiene la compatibilidad?
> 3. ¿Hay tests que probar?
> 4. ¿Documenté el cambio?
>
> Si respondiste NO a alguna, pregunta al usuario primero.

---

**Versión:** 1.0  
**Última Actualización:** 2025-01-14  
**Mantenedor:** Ver .env o configuración del proyecto