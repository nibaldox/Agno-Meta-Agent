# 📚 Documentación General del Meta-Agente

## 1. Introducción

El proyecto **Meta-Agente Generador de Agentes AI** automatiza la creación de agentes especializados basados en el framework Agno. El sistema conversa con la persona usuaria, analiza requisitos, genera un plan validado con Pydantic y produce código Python listo para ejecutarse.

## 2. Estado Actual del Proyecto

- Marco base funcionando en `src/application/services/meta_agent.py`, con los agentes Analyzer y Planner configurados sobre modelos DeepSeek.
- Templates para generación de código ubicadas en `src/infrastructure/templates/agent_templates.py`, cubriendo agentes básicos, con memoria y equipos colaborativos.
- CLI interactiva disponible en `src/presentation/cli/main.py` para guiar la creación de agentes desde terminal.
- Carpeta `generated/agents` con ejemplos operativos de agentes producidos automáticamente.
- Documentación operativa y prompts iniciales reubicados en la nueva carpeta `dics/`.

## 3. Arquitectura Resumida

- **Application (`src/application/`)**: Contiene los servicios del meta-agente. El archivo clave `services/meta_agent.py` orquesta el análisis de requisitos, la planificación y la generación de código. Incluye la clase `AgentPlan` basada en Pydantic y el flujo interactivo con Rich.
- **Infrastructure/Templates (`src/infrastructure/templates/`)**: Aloja `agent_templates.py` con métodos estáticos que traducen especificaciones del plan en código Python. Gestiona imports dinámicos de herramientas, elección de modelo y variantes de agentes (básico, con memoria, equipos).
- **Presentation (`src/presentation/cli/`)**: Provee la interfaz de línea de comandos (`main.py`) que instacia `MetaAgent` y ejecuta el flujo `interactive_creation()` para guiar a la persona usuaria.
- **Generated (`generated/`)**: Contiene ejemplos reales de agentes creados y sirve como carpeta de salida por defecto. `generated/agents/` almacena los scripts Python generados.
- **Docs (`dics/`)**: Repositorio documental que centraliza contexto, prompts, bitácora y guías de referencia.

### 3.1 Detalle por Módulo

- **Analyzer Agent** (`MetaAgent.analyze_request`): Emplea el modelo DeepSeek Chat para identificar vacíos de información y formular preguntas específicas. Utiliza prompts estructurados con ejemplos guiados.
- **Planner Agent** (`MetaAgent.create_plan`): Crea un JSON conforme al esquema `AgentPlan` utilizando DeepSeek Reasoner. Incluye lógica para limpiar respuestas con formato markdown y validación robusta.
- **Templates** (`AgentTemplate`): Proporciona funciones `generate_basic_agent`, `generate_agent_with_memory`, `generate_agent_team`. Se basan en f-strings multilínea, calculan imports necesarios y ensamblan configuraciones de agentes Agno.
- **Persistencia**: Los agentes con memoria emplean `SqliteAgentStorage` y `AgentMemory` de Agno. Los archivos generados se guardan en `generated/agents` con codificación UTF-8.

## 4. Próximos Pasos de Documentación

- Completar guías detalladas por módulo (Application, Infrastructure, Presentation) incluyendo diagramas simples de flujo.
- Documentar el flujo de conversación paso a paso con ejemplos extendidos y recomendaciones de prompting.
- Añadir sección de troubleshooting y mejores prácticas para extender templates (ver sección 6).
- Incorporar checklist de pruebas manuales y plan futuro de tests automatizados (secciones 5.2 y 5.3).

## 5. Estrategia de Calidad

### 5.1 Consideraciones Generales

- Validar que cada agente generado incluya imports correctos, configuración de modelo coherente y manejo de herramientas adecuado.
- Mantener consistencia en docstrings, type hints y estilo PEP 8.
- Registrar cada iteración relevante en `dics/bitacora_map.md` para asegurar trazabilidad.
- Ejecutar pruebas automatizadas con `pytest` y reporte de cobertura (`pytest --cov=src --cov-report=term-missing`).
- Verificar entorno de desarrollo con `pip install -r requirements-dev.txt` antes de correr la suite.

### 5.2 Plan de Pruebas Manuales (Resumen)

- Verificar flujo interactivo CLI: preguntas aclaratorias, confirmación y generación de archivo.
- Generar agentes en los tres niveles disponibles (básico, memoria, equipo) y ejecutar los scripts resultantes con dependencias configuradas.
- Validar memoria persistente: confirmar creación y reutilización de `agents_memory.sqlite`.
- Revisar herramientas soportadas (DuckDuckGo, YFinance, Reasoning, Python, File) asegurando que las plantillas generen imports e inicialización correctas.
- Evaluar robustez ante entradas incompletas: asegurar que el analyzer solicite información faltante sin bucles infinitos.

### 5.3 Plan de Suite Automatizada (Resumen)

- Diseñar tests unitarios para `AgentTemplate` cubriendo generación de código según especificaciones mínimas y completas.
- Implementar tests para `MetaAgent.create_plan` usando respuestas mockeadas del planner que ejerciten la limpieza y validación de JSON (en progreso: ver `tests/test_meta_agent.py`).
- Crear pruebas de integración que simulen flujo completo `interactive_creation` mediante dependencia inyectada o mocks de `Agent`.
- Establecer objetivo de cobertura >80% en módulos críticos (`meta_agent.py`, `agent_templates.py`).
- Configurar pipeline futuro (Pytest + Coverage) integrable con CI.

### 5.4 Avance Actual (2025-10-14)

- Suite automatizada ejecutable con `pytest` (configuración en `pytest.ini` con cobertura 88%).
- Cobertura aproximada: `meta_agent.py` 85%, `agent_templates.py` 90%.
- Módulos de pruebas principales: `tests/test_agent_templates.py`, `tests/test_meta_agent.py`.
- Configuración de pytest centralizada y `.coveragerc` con exclusiones para rutas aún no cubiertas.

## 6. Troubleshooting y Mejores Prácticas

- **Planner devuelve texto adicional**: Revisar limpieza en `create_plan`. Utilizar regex y manejo de markdown como ya implementado; si persiste, registrar contenido en consola y ajustar prompt.
- **Herramienta no reconocida**: Asegurarse de actualizar los mapas en `_get_tool_import` y `_generate_tools_init` dentro de `agent_templates.py`.
- **Errores de encoding al guardar**: Confirmar uso de `encoding="utf-8"` al escribir archivos y rutas válidas en Windows.
- **Preguntas repetitivas del analyzer**: Revisar prompt en `analyze_request`, añadir ejemplos específicos o ampliar contexto si la conversación no se acumula correctamente.
- **Agente con memoria falla**: Verificar creación de `SqliteAgentStorage` con rutas relativas válidas y permisos de escritura.

## 5. Recursos Relevantes

- `dics/proyect_context.md`: Contexto y normas de contribución para Cursor AI.
- `dics/cursor_prompts.md`: Prompts sugeridos para tareas comunes.
- `README.md`: Presentación general y guía de uso del proyecto.

