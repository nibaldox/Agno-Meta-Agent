# 🎯 Guía de Prompts para Cursor - Meta-Agente

Esta guía contiene prompts optimizados para trabajar con Cursor AI en el proyecto Meta-Agente.

---

## 🏗️ PROMPTS DE CONSTRUCCIÓN

### Crear Nueva Plantilla de Agente

```
# TAREA: Crear plantilla para agentes con búsqueda de conocimiento (RAG)

CONTEXTO:
- Archivo: agent_templates.py
- Patrón base: generate_agent_with_memory() líneas 72-120
- Nuevo método: generate_agent_with_knowledge()

REQUISITOS:
1. Importar AgentKnowledge desde agno.knowledge
2. Configurar vector database (usar PgVector por default)
3. Incluir document loaders
4. Seguir mismo patrón de retorno que otros métodos

CÓDIGO ESPERADO:
- Type hints completos
- Docstring descriptivo
- Manejo de spec con .get() y defaults
- Código generado válido y ejecutable

REFERENCIAS:
- Agno docs sobre knowledge: https://docs.agno.com/agents/knowledge
- Patrón existente: línea 72 de agent_templates.py
```

### Añadir Soporte para Nueva Herramienta

```
# TAREA: Añadir soporte para GitHub Tools

CONTEXTO:
- Archivo: agent_templates.py
- Funciones a modificar: _get_tool_import() y _generate_tools_init()
- Patrón: ver líneas 200-235

IMPLEMENTACIÓN:
1. En _get_tool_import():
   - Añadir entrada: 'github': 'from agno.tools.github import GithubTools'
   - Mapear variantes: 'git', 'repository', 'repo'

2. En _generate_tools_init():
   - Detectar 'github' en tool_lower
   - Retornar: 'GithubTools()'

VALIDACIÓN:
- Crear agente test con herramienta GitHub
- Verificar que el código generado compile
- Probar que el import funcione
```

### Mejorar Análisis de Solicitudes

```
# TAREA: Hacer el analyzer_agent más inteligente

CONTEXTO:
- Archivo: meta_agent.py
- Método: analyze_request() línea 38
- Problema actual: A veces hace preguntas redundantes

OBJETIVO:
Mejorar el prompt del analyzer_agent para que:
1. Detecte cuando ya tiene suficiente información
2. Haga preguntas más específicas y contextuales
3. Sugiera opciones concretas al usuario
4. No repita preguntas sobre info ya proporcionada

ENFOQUE:
- Mantener estructura actual del prompt
- Añadir ejemplos de buenas vs malas preguntas
- Incluir lógica para detectar INFO_COMPLETA más efectivamente
- Usar few-shot learning en el prompt

EJEMPLO OUTPUT ESPERADO:
"Entiendo que necesitas un agente financiero. Basándome en tu descripción:
1. ¿Prefieres análisis de acciones individuales o comparación de mercados?
2. ¿Qué frecuencia de datos: diaria, semanal, o tiempo real?
Responde con los números para ir más rápido (ej: 1a, 2c)"
```

---

## 🔧 PROMPTS DE REFACTORIZACIÓN

### Optimizar Generación de Código

```
# TAREA: Refactorizar sistema de templates para mejor mantenibilidad

PROBLEMA ACTUAL:
- Mucha duplicación de código entre templates
- Lógica de imports repetida en cada método
- Difícil añadir nuevas features globalmente

PROPUESTA:
1. Extraer lógica común a métodos auxiliares privados:
   - _build_imports(spec) → retorna string de imports
   - _build_agent_config(spec) → retorna string de configuración
   - _build_example_usage(spec) → retorna string de ejemplo

2. Refactorizar generate_*_agent() para usar helpers:
   ```python
   def generate_basic_agent(spec: Dict) -> str:
       imports = self._build_imports(spec)
       config = self._build_agent_config(spec)
       example = self._build_example_usage(spec)
       return self._assemble_code(imports, config, example)
   ```

3. Mantener compatibilidad: No cambiar firmas públicas

RESULTADO ESPERADO:
- Menos líneas de código total
- Más fácil añadir features
- Misma funcionalidad externa
- Tests pasan (cuando los creemos)
```

### Mejorar Manejo de Errores

```
# TAREA: Añadir manejo robusto de errores

CONTEXTO:
- Archivo: meta_agent.py
- Métodos: create_plan(), generate_code(), interactive_creation()

PROBLEMAS ACTUALES:
1. JSON parsing puede fallar silenciosamente
2. No hay validación de spec antes de generar código
3. Errores genéricos poco informativos

SOLUCIÓN PROPUESTA:
1. En create_plan():
   - Try/catch específico para JSONDecodeError
   - Logging del contenido problemático
   - Retry con prompt clarificado
   - Mensaje de error útil al usuario

2. En generate_code():
   - Validar spec antes de generar
   - Verificar campos requeridos
   - Custom exceptions: InvalidSpecError, TemplateError

3. En interactive_creation():
   - Wrappear con try/catch comprehensivo
   - Guardar estado en caso de error
   - Ofrecer retry o debug info

PATRÓN:
```python
try:
    # operación
except SpecificError as e:
    logger.error(f"Context: {context}", exc_info=True)
    console.print(f"[red]Error específico: {e}[/red]")
    # recovery logic
```
```

---

## 🧪 PROMPTS DE TESTING

### Crear Tests Unitarios

```
# TAREA: Crear suite de tests para agent_templates.py

CONTEXTO:
- Framework: pytest
- Archivo nuevo: tests/test_agent_templates.py
- Cobertura objetivo: >80%

ESTRUCTURA:
```python
import pytest
from agent_templates import AgentTemplate

class TestAgentTemplate:
    def test_generate_basic_agent_minimal_spec(self):
        """Test con spec mínimo requerido"""
        spec = {
            'nombre': 'Test Agent',
            'rol': 'Testing',
            'descripcion': 'Test',
            'ejemplo_uso': 'test'
        }
        code = AgentTemplate.generate_basic_agent(spec)
        assert 'Agent(' in code
        assert 'Test Agent' in code
    
    def test_generate_basic_agent_with_tools(self):
        """Test con herramientas"""
        # ...
    
    def test_get_model_import_claude(self):
        """Test mapeo de modelos"""
        # ...
```

CASOS A CUBRIR:
1. Specs mínimos vs completos
2. Cada tipo de modelo soportado
3. Cada herramienta soportada
4. Equipos de agentes
5. Edge cases: specs vacíos, None values
```

### Crear Tests de Integración

```
# TAREA: Tests end-to-end del flujo completo

ARCHIVO: tests/test_integration.py

ESCENARIOS:
1. Flujo completo: solicitud → plan → código → ejecución
2. Múltiples iteraciones de preguntas
3. Generación de diferentes tipos de agentes
4. Manejo de solicitudes ambiguas

EJEMPLO:
```python
def test_full_workflow_web_search_agent():
    """Test generación de agente de búsqueda web"""
    meta = MetaAgent()
    
    # Simular conversación
    conversation = """
    Usuario: Necesito un agente que busque en internet
    Asistente: ¿Qué tipo de búsquedas?
    Usuario: Noticias de tecnología, sin memoria
    """
    
    plan = meta.create_plan(conversation)
    
    assert plan.nombre is not None
    assert 'duckduckgo' in plan.herramientas
    assert plan.necesita_memoria == False
    
    code = meta.generate_code(plan)
    
    # Verificar que el código es válido
    compile(code, '<string>', 'exec')
    
    # Verificar estructura esperada
    assert 'from agno.agent import Agent' in code
    assert 'DuckDuckGoTools' in code
```
```

---

## 🎨 PROMPTS DE UI/UX

### Mejorar Interfaz CLI

```
# TAREA: Hacer la interfaz más amigable y visual

CONTEXTO:
- Archivo: meta_agent.py → interactive_creation()
- Librería: Rich (ya instalada)

MEJORAS PROPUESTAS:
1. Progress bar durante generación:
   ```python
   with console.status("[bold green]Analizando solicitud...") as status:
       analysis = self.analyze_request(conversation)
   ```

2. Tabla para mostrar el plan:
   ```python
   from rich.table import Table
   table = Table(title="Plan del Agente")
   table.add_column("Campo", style="cyan")
   table.add_column("Valor", style="green")
   table.add_row("Nombre", plan.nombre)
   # ...
   console.print(table)
   ```

3. Syntax highlighting para código:
   ```python
   from rich.syntax import Syntax
   syntax = Syntax(code, "python", theme="monokai")
   console.print(syntax)
   ```

4. Prompt estilo wizard:
   - Números de paso más visuales
   - Opciones con letras (a, b, c)
   - Help text contextual

REFERENCIAS:
- Rich docs: https://rich.readthedocs.io/en/latest/
```

### Añadir Modo Interactivo Avanzado

```
# TAREA: Crear modo wizard con selección visual

FUNCIONALIDAD:
- Usar rich.prompt.Prompt para inputs mejorados
- Menú de selección con rich.prompt.Confirm
- Questionary-style para opciones múltiples

EJEMPLO:
```python
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console

console = Console()

# Tipo de agente
agent_type = Prompt.ask(
    "Tipo de agente",
    choices=["individual", "equipo", "workflow"],
    default="individual"
)

# Herramientas (múltiple selección)
console.print("\n[bold]Herramientas disponibles:[/bold]")
available_tools = [
    "1. Búsqueda web (DuckDuckGo)",
    "2. Finanzas (YFinance)",
    "3. Razonamiento (Reasoning)",
    "4. Código (Python)",
]
for tool in available_tools:
    console.print(f"  {tool}")

tools_input = Prompt.ask(
    "\nSelecciona herramientas (números separados por coma)",
    default="1"
)
```
```

---

## 📊 PROMPTS DE ANÁLISIS

### Analizar Calidad del Código Generado

```
# TAREA: Auditar calidad del código que genera el meta-agente

ANÁLISIS REQUERIDO:
1. ¿El código generado sigue PEP 8?
2. ¿Tiene docstrings adecuados?
3. ¿Maneja errores apropiadamente?
4. ¿Es eficiente y no tiene redundancias?
5. ¿Es seguro (no ejecuta código arbitrario)?

MÉTODO:
1. Generar 10 agentes diferentes
2. Revisar el código producido
3. Identificar patrones problemáticos
4. Sugerir mejoras a las templates

OUTPUT ESPERADO:
- Reporte con issues encontrados
- Ranking de severidad
- Propuestas de fix
- Código refactorizado si aplica
```

### Optimizar Performance

```
# TAREA: Profiling del meta-agente

OBJETIVO: Identificar bottlenecks

PASOS:
1. Usar cProfile para medir:
   ```python
   import cProfile
   profiler = cProfile.Profile()
   profiler.enable()
   # código del meta-agente
   profiler.disable()
   profiler.print_stats(sort='cumulative')
   ```

2. Áreas a revisar:
   - Tiempo de respuesta del analyzer_agent
   - Parsing de JSON
   - Generación de templates
   - File I/O

3. Optimizaciones posibles:
   - Cache de respuestas comunes
   - Async para llamadas a LLM
   - Lazy loading de templates
   - Memoización de funciones puras

DELIVERABLE:
- Reporte de profiling
- Lista de optimizaciones
- Implementación de mejoras
- Benchmarks antes/después
```

---

## 🚀 PROMPTS DE FEATURES NUEVAS

### Añadir Modo Batch

```
# TAREA: Crear modo batch para generar múltiples agentes

CONTEXTO:
- Archivo nuevo: batch_generator.py
- Input: YAML o JSON con múltiples specs
- Output: Múltiples archivos .py

DISEÑO:
```python
# agents_batch.yaml
agents:
  - nombre: "Buscador Web"
    rol: "Buscar información"
    herramientas: ["duckduckgo"]
    
  - nombre: "Analista Financiero"
    rol: "Analizar acciones"
    herramientas: ["yfinance"]
```

```python
# batch_generator.py
from meta_agent import MetaAgent
import yaml

def generate_from_batch(yaml_file: str):
    with open(yaml_file) as f:
        config = yaml.safe_load(f)
    
    meta = MetaAgent()
    results = []
    
    for spec in config['agents']:
        plan = AgentPlan(**spec)
        code = meta.generate_code(plan)
        # guardar y reportar
        results.append(...)
    
    return results
```

USO:
```bash
python batch_generator.py agents_batch.yaml --output ./generated/
```
```

### Añadir Validación Pre-generación

```
# TAREA: Validar specs antes de generar código

PROBLEMA:
- A veces se generan agentes con configuraciones inválidas
- No hay validación de compatibilidad herramientas-modelo
- Specs incompletos pasan sin warning

SOLUCIÓN:
Crear AgentValidator en nuevo archivo validators.py:

```python
class AgentValidator:
    """Valida especificaciones de agentes"""
    
    @staticmethod
    def validate_plan(plan: AgentPlan) -> List[ValidationError]:
        errors = []
        
        # Validar nombre
        if not plan.nombre or len(plan.nombre) < 3:
            errors.append(ValidationError("Nombre muy corto"))
        
        # Validar compatibilidad herramientas-modelo
        if plan.modelo == "claude" and "browser" in plan.herramientas:
            errors.append(ValidationError(
                "Claude no soporta browser tools directamente"
            ))
        
        # Validar nivel vs features
        if plan.nivel == 1 and plan.necesita_memoria:
            errors.append(ValidationError(
                "Nivel 1 no soporta memoria, usar nivel 3+"
            ))
        
        return errors
```

INTEGRACIÓN:
- Llamar en generate_code() antes de generar
- Mostrar errores al usuario
- Sugerir correcciones
```

---

## 🤖 PROMPTS META (Para Mejorar Este Sistema)

### Auto-mejora del Meta-Agente

```
# TAREA: Hacer que el meta-agente se pueda auto-mejorar

CONCEPTO:
El meta-agente debería poder:
1. Analizar agentes que ha generado
2. Identificar patrones comunes
3. Sugerir mejoras a sus propias templates
4. Generar nuevas templates automáticamente

IMPLEMENTACIÓN:
```python
class SelfImprovingMetaAgent(MetaAgent):
    def analyze_generated_agents(self, agents_dir: str):
        """Analiza agentes generados para encontrar patrones"""
        patterns = []
        # leer todos los .py
        # extraer configuraciones comunes
        # identificar oportunidades de templates nuevos
        return patterns
    
    def suggest_template_improvements(self):
        """Sugiere mejoras basadas en uso real"""
        # analizar qué features se usan más
        # detectar configuraciones repetidas
        # proponer nuevas abstracciones
        pass
```

META: Este es un prompt para que Cursor te ayude a hacer el sistema más inteligente
```

---

## 📖 GUÍA DE USO DE ESTOS PROMPTS

### Cómo Usar Efectivamente

1. **Copia el prompt completo** - No lo modifiques, está optimizado
2. **Pégalo en Cursor** - Usa Cmd/Ctrl+L para abrir chat
3. **Añade contexto específico** si es necesario
4. **Revisa el código generado** - Cursor no es infalible
5. **Itera** - Si no funciona a la primera, refina el prompt

### Estructura de un Buen Prompt

```
# TAREA: [Qué hacer - específico]

CONTEXTO: [Dónde, qué archivos, qué estado actual]

REQUISITOS: [Lista numerada de lo que debe cumplir]

CÓDIGO/EJEMPLO: [Si aplica, código de referencia]

REFERENCIAS: [Links o líneas de código relevantes]
```

### Tips para Cursor

- **Sé específico**: "Modifica línea 42" > "Mejora el código"
- **Da ejemplos**: Muestra lo que quieres
- **Referencia código existente**: "Como en línea X"
- **Especifica constraints**: "Sin cambiar la API pública"
- **Pide explicaciones**: "¿Por qué este approach?"

---

## 🎓 EJERCICIOS PRÁCTICOS

Para familiarizarte con el proyecto, intenta estos ejercos usando Cursor:

### Nivel Básico
1. Añadir soporte para una nueva herramienta simple
2. Mejorar un mensaje de error
3. Añadir un campo nuevo a AgentPlan

### Nivel Intermedio
4. Crear una nueva plantilla de agente
5. Refactorizar una función duplicada
6. Añadir tests para un método

### Nivel Avanzado
7. Implementar modo batch
8. Añadir API REST
9. Crear sistema de plugins para templates

---

**¿Necesitas más prompts?** Pídele a Cursor:
```
Basándote en CURSOR_PROMPTS.md, genera un prompt para [tu tarea específica]
```

**Última actualización:** 2025-01-14