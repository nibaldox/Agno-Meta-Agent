# 🎯 Integración con Cursor IDE - Meta-Agente

Esta guía te ayudará a configurar Cursor AI para trabajar óptimamente con este proyecto.

---

## 🚀 Setup Rápido (5 minutos)

### Paso 1: Añadir Documentación a Cursor

Cursor puede indexar documentación externa para ayudarte mejor:

1. Abre **Cursor Settings** (Cmd/Ctrl + ,)
2. Ve a **Features** → **Docs**
3. Haz clic en **Add new doc**
4. Añade estas URLs:

```
Documentación de Agno:
https://docs.agno.com/llms-full.txt

Documentación de Pydantic:
https://docs.pydantic.dev/latest/

Documentación de Rich:
https://raw.githubusercontent.com/Textualize/rich/master/README.md
```

### Paso 2: Configurar Reglas del Proyecto

Crea un archivo `.cursorrules` en la raíz del proyecto con este contenido:

```
# Meta-Agente Generator - Cursor AI Rules

## Project Context
Este es un proyecto de generación automática de agentes AI usando el framework Agno.
El meta-agente conversa con usuarios para crear agentes personalizados.

## Critical Files
- meta_agent.py: Lógica principal del orquestador
- agent_templates.py: Sistema de templates para generar código
- main.py: Punto de entrada CLI

## Code Standards
- Python 3.10+, PEP 8 estricto
- Type hints OBLIGATORIOS en todas las funciones públicas
- Docstrings en formato Google
- Usar Pydantic para validación de datos
- Usar Rich para output en terminal

## Framework Context
- Agno Framework: https://docs.agno.com
- Siempre importar: from agno.agent import Agent
- Modelos: Claude (Anthropic), GPT-4 (OpenAI), Gemini (Google)

## When Generating Code
- Seguir patrones en agent_templates.py
- Usar f-strings para código generado
- Mantener compatibilidad con API existente
- No romper código ya generado

## When Refactoring
- NO cambiar firmas públicas sin confirmar
- Mantener type hints actualizados
- Actualizar docstrings si cambia comportamiento

## Testing
- Preferir pytest
- Cobertura mínima: 70%
- Tests en carpeta tests/

Leer PROJECT_CONTEXT.md para detalles completos.
```

### Paso 3: Configurar Composer (Chat Multi-Archivo)

Cursor Composer te permite editar múltiples archivos a la vez. Configúralo:

1. Abre Composer (Cmd/Ctrl + I)
2. Añade estos archivos por default:
   - `meta_agent.py`
   - `agent_templates.py`
   - `PROJECT_CONTEXT.md` (como referencia)

---

## 🎨 Prompts Optimizados para Cursor

### Comando: Analizar Código

```
@Codebase Analiza la arquitectura completa del meta-agente y dame un resumen de:
1. Flujo principal de ejecución
2. Patrones de diseño utilizados
3. Dependencias entre componentes
4. Posibles mejoras
```

### Comando: Generar Tests

```
@meta_agent.py Genera tests unitarios completos para la clase MetaAgent.
Usa pytest, incluye mocks para los agentes internos, y cubre todos los métodos públicos.
Guarda en tests/test_meta_agent.py
```

### Comando: Refactorizar

```
@agent_templates.py Refactoriza el método generate_basic_agent() para extraer
la lógica de construcción de imports a un método privado _build_imports().
Mantén la misma funcionalidad y API pública.
```

### Comando: Documentar

```
@Codebase Genera documentación API completa en formato Markdown.
Incluye: clases, métodos públicos, parámetros, retornos, ejemplos.
Guarda en docs/API.md
```

### Comando: Debugging

```
@meta_agent.py línea 120: El JSON parsing a veces falla.
Analiza el problema y propón una solución más robusta que:
1. Detecte JSON malformado
2. Intente múltiples estrategias de limpieza
3. Log el problema
4. Dé feedback útil al usuario
```

---

## 🛠️ Atajos de Cursor para Este Proyecto

### Navegación Rápida

| Atajo | Acción |
|-------|--------|
| `Cmd+P` | Buscar archivo rápido |
| `Cmd+Shift+F` | Buscar en todo el proyecto |
| `Cmd+Click` | Ir a definición |
| `Cmd+K` → `Cmd+R` | Ver referencias |

### AI Features

| Atajo | Acción |
|-------|--------|
| `Cmd+K` | Inline edit (editar código seleccionado) |
| `Cmd+L` | Abrir chat lateral |
| `Cmd+I` | Abrir Composer (multi-archivo) |
| `Cmd+Shift+L` | Ver historial de cambios AI |

### Workflow Recomendado

1. **Explorar**: Usa `@Codebase` para entender el proyecto
2. **Planear**: Usa Chat para discutir el cambio
3. **Implementar**: Usa Composer para cambios multi-archivo
4. **Refinar**: Usa Inline Edit para ajustes pequeños
5. **Revisar**: Lee los diffs antes de aceptar

---

## 📚 Comandos Útiles con @

### @Codebase - Buscar en Todo el Proyecto

```
@Codebase ¿Dónde se define AgentPlan?
@Codebase Muéstrame todos los usos de generate_basic_agent
@Codebase ¿Qué archivos importan desde agent_templates?
```

### @File - Referencia Específica

```
@meta_agent.py Explica el método interactive_creation()
@agent_templates.py ¿Cómo se mapean las herramientas a imports?
@main.py ¿Cómo se validan las variables de entorno?
```

### @Docs - Usar Documentación Externa

```
@Docs Agno ¿Cómo creo un agente con memoria?
@Docs Pydantic ¿Cómo valido campos opcionales?
@Docs Rich ¿Cómo creo una tabla con colores?
```

### @Web - Buscar Información Actual

```
@Web ¿Cuáles son las últimas features de Agno?
@Web Ejemplos de agentes multi-modal con Agno
@Web Best practices para prompts de AI agents
```

---

## 💡 Workflows Comunes

### Workflow 1: Añadir Nueva Feature

```bash
# 1. Analizar impacto
@Codebase Si añado soporte para [FEATURE], ¿qué archivos necesito modificar?

# 2. Implementar
@Composer 
TAREA: Añadir soporte para [FEATURE]
ARCHIVOS: [lista de archivos del paso 1]
REQUISITOS: [lista de requisitos]

# 3. Validar
@File tests/test_FEATURE.py
Genera tests para la nueva feature

# 4. Documentar
@File PROJECT_CONTEXT.md
Actualiza la sección de features para incluir [FEATURE]
```

### Workflow 2: Debugging

```bash
# 1. Identificar el problema
@Codebase ¿Dónde se maneja [COMPORTAMIENTO]?

# 2. Analizar
@File [archivo].py línea [X]
Explica qué hace este código y por qué podría fallar

# 3. Proponer solución
@Codebase Propón una solución para [PROBLEMA] que:
- Mantenga compatibilidad
- Añada logging
- Maneje edge cases

# 4. Implementar
@Composer Implementa la solución en [archivos afectados]
```

### Workflow 3: Refactoring

```bash
# 1. Detectar code smells
@Codebase Identifica código duplicado o patrones anti-pattern

# 2. Planear refactor
@Codebase Propón un plan de refactoring para [COMPONENTE]
que mejore [ASPECTO] sin romper funcionalidad

# 3. Ejecutar
@Composer 
REFACTOR: [descripción]
ARCHIVOS: [lista]
MANTENER: API pública, tests pasan

# 4. Verificar
@Codebase ¿El refactor introduce nuevas dependencias o side effects?
```

---

## 🎓 Tips Pro para Cursor

### 1. Contexto es Rey

**Mal prompt:**
```
Mejora este código
```

**Buen prompt:**
```
@agent_templates.py líneas 150-180
Refactoriza _get_tool_import() para:
1. Usar diccionario en lugar de if-elif
2. Soportar aliases de herramientas
3. Retornar tuple (import, init_code)
Mantén la API pública sin cambios.
```

### 2. Usa Referencias Cruzadas

```
@meta_agent.py Implementa validación de plan similar a como
@agent_templates.py valida spec en línea 250
```

### 3. Iteración con Apply

Cuando Cursor sugiere cambios:
- ✅ **Lee el diff completo** antes de aplicar
- ✅ **Aplica en chunks** si son muchos cambios
- ✅ **Testea después de cada apply**
- ❌ **No apliques ciegamente** todo a la vez

### 4. Memoria de Conversación

Cursor recuerda el contexto en la misma conversación:

```
Tu: @Codebase Analiza cómo funcionan las templates

[Cursor responde con análisis detallado]

Tu: Ahora crea una nueva template siguiendo ese patrón
para agentes con [FEATURE]

[Cursor usa el contexto de su análisis previo]
```

### 5. Composer para Cambios Grandes

Para features que afectan múltiples archivos:

```
@Composer

FEATURE: Añadir modo batch para generar múltiples agentes

ARCHIVOS:
- batch_generator.py (nuevo)
- meta_agent.py (modificar)
- main.py (añadir comando)
- tests/test_batch.py (nuevo)

DISEÑO:
[explicación del diseño]

REQUISITOS:
1. Leer YAML con specs
2. Generar todos los agentes
3. Reportar errores
4. Mantener compatibilidad con modo individual
```

---

## 🐛 Troubleshooting Cursor

### Problema: Cursor no encuentra archivos del proyecto

**Solución:**
1. Reinicia Cursor
2. Verifica que estás en la raíz del proyecto
3. Indexa manualmente: Cmd+Shift+P → "Reindex"

### Problema: Cursor genera código que no funciona

**Causas comunes:**
- No tiene contexto suficiente → Usa @File o @Codebase
- No conoce Agno → Verifica que añadiste la doc de Agno
- Usa información desactualizada → Especifica versiones

**Solución:**
```
@Docs Agno @File agent_templates.py

Genera [CÓDIGO] usando Agno 2.0+ y siguiendo el patrón
en generate_basic_agent()
```

### Problema: Cambios rompen funcionalidad existente

**Prevención:**
1. Siempre pide que mantenga API pública
2. Especifica qué tests deben pasar
3. Usa Apply selectivamente

**Fix:**
```
@Codebase El último cambio rompió [FUNCIONALIDAD].
Revierte el cambio y propón alternativa que:
- No cambie la firma de funciones públicas
- Pase todos los tests existentes
- Logre el objetivo original
```

---

## 📊 Métricas de Éxito con Cursor

Usa Cursor efectivamente cuando:

- ✅ **Generas código en minutos** vs horas manualmente
- ✅ **El código generado sigue** los patrones del proyecto
- ✅ **Tests pasan** después de aplicar cambios
- ✅ **Entiendes el código** que Cursor genera
- ✅ **Iteras rápido** entre idea → implementación

Si no logras esto:
- 📖 Lee PROJECT_CONTEXT.md más a fondo
- 🎯 Usa prompts más específicos
- 🔍 Verifica que Cursor tiene el contexto correcto
- 💬 Haz preguntas a Cursor sobre el proyecto primero

---

## 🎯 Ejercicios de Práctica

### Nivel 1: Familiarización

1. **Explorar**: `@Codebase Explica la arquitectura del meta-agente`
2. **Buscar**: `@Codebase ¿Dónde se valida el AgentPlan?`
3. **Modificar**: Usa Inline Edit para mejorar un docstring

### Nivel 2: Implementación

4. **Nueva función**: Añade método helper en agent_templates.py
5. **Tests**: Genera tests para un método existente
6. **Debugging**: Corrige un bug con ayuda de Cursor

### Nivel 3: Features Completas

7. **Mini-feature**: Añade soporte para nueva herramienta
8. **Refactor**: Mejora una función duplicada
9. **Documentación**: Genera docs completas con Cursor

---

## 🔗 Enlaces Útiles

- **Cursor Docs:** https://docs.cursor.com
- **Agno Docs:** https://docs.agno.com  
- **Este Proyecto:**
  - `PROJECT_CONTEXT.md` - Contexto completo
  - `CURSOR_PROMPTS.md` - Biblioteca de prompts
  - `.cursorrules` - Reglas del proyecto

---

## 💬 Ayuda

**¿Cursor hace algo inesperado?**

Resetea el contexto:
1. Cmd+Shift+P → "Clear Chat History"
2. Cierra y abre Cursor
3. Empieza nueva conversación con contexto claro

**¿Necesitas ayuda con un prompt?**

Pregunta a Cursor:
```
@CURSOR_PROMPTS.md Dame un prompt para [tu tarea específica]
```

---

**¡Listo para ser ultra-productivo con Cursor!** 🚀

Empieza con: `@Codebase Dame un tour del proyecto meta-agente`