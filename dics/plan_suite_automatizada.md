# 🤖 Plan de Suite de Pruebas Automatizadas

## 1. Objetivo

Diseñar una estrategia de pruebas automatizadas que cubra las piezas críticas del meta-agente, garantice regresiones controladas y facilite la integración continua.

## 2. Alcance Inicial

- Tests unitarios para `src/infrastructure/templates/agent_templates.py`.
- Tests unitarios y de integración ligera para `src/application/services/meta_agent.py`.
- Validación sintáctica del código generado (compilación estática) y verificación de configuraciones.

## 3. Herramientas y Frameworks Propuestos

- Pytest como runner principal.
- pytest-mock o unittest.mock para simular respuestas de los agentes DeepSeek.
- Coverage.py para medición de cobertura (objetivo ≥ 80% en módulos críticos).
- pre-commit con hooks opcionales para linting (black, isort, flake8) a mediano plazo.

## 4. Estructura Sugerida de Directorios

```
tests/
├── __init__.py
├── test_agent_templates.py
├── test_meta_agent.py
└── fixtures/
    ├── __init__.py
    └── planner_responses.py  # JSON de ejemplo para mockear respuestas
```

## 5. Plan por Tipo de Prueba

### 5.1 Tests Unitarios: `AgentTemplate`

- `test_generate_basic_agent_minimal_spec`: Validar generación base con especificación mínima.
- `test_generate_basic_agent_with_tools`: Comprobar imports y configuración de herramientas.
- `test_generate_agent_with_memory`: Asegurar inclusión de memoria y storage.
- `test_generate_agent_team`: Verificar estructura de equipos y uso de modelos alternos.
- `test_tool_mapping_unknown`: Garantizar manejo controlado para herramientas no soportadas.

### 5.2 Tests Unitarios: `MetaAgent`

- Mockear `analyzer_agent` y `planner_agent` para aislar lógica propia.
- `test_create_plan_valid_json`: Verificar parsing exitoso de JSON limpio.
- `test_create_plan_markdown_wrapped`: Asegurar extracción correcta de JSON cuando viene en bloques ```json```.
- `test_generate_code_branching`: Confirmar selección de template según `nivel`, `necesita_memoria`, `es_equipo`.
- `test_generate_code_model_adjustment`: Validar ajuste de modelo a `deepseek-reasoner` para equipos.

### 5.3 Tests de Integración Ligera

- Simular `interactive_creation` con entradas controladas utilizando `monkeypatch` o `capsys` para validar mensajes y archivo generado sin ejecutar modelos reales.
- Test para confirmar escritura en `generated/agents/` y contenido del archivo resultante.

## 6. Casos Negativos y Bordes

- Planner devolviendo JSON inválido → `create_plan` debe arrojar `ValueError` con mensaje claro.
- Especificación faltante de herramientas → Templates deben manejar listas vacías sin fallar.
- Tool no soportada → Verificar que se lanza excepción o se ignora con advertencia (definir comportamiento esperado).

## 7. Integración con CI (Futuro)

- Configurar workflow de GitHub Actions (o alternativa) que ejecute:
  - `pip install -r requirements.txt`
  - `pip install -r requirements-dev.txt` (a crear)
  - `pytest --cov=src --cov-report=xml`
- Publicar reporte de cobertura y fallar pipeline si cobertura < umbral definido.

## 8. Roadmap de Implementación

1. Crear carpeta `tests/` con estructura mínima y configurar `pytest.ini`. ✅ (2025-10-14)
2. Implementar tests unitarios de templates (prioridad alta, impacto bajo en tiempo). ✅
3. Añadir mocks para planner/analyzer y cubrir lógica de `MetaAgent`. ✅
4. Diseñar pruebas de integración para CLI utilizando `capsys` y `tmp_path`. ✅
5. Introducir medición de cobertura y ajustar umbrales. ✅ (cobertura actual 86%)
6. Integrar pipeline de CI con ejecución automática en cada push/PR. ✅ (`.github/workflows/tests.yml`)

## 9. Métricas de Éxito

- Cobertura ≥ 80% en `meta_agent.py` y `agent_templates.py`.
- Tiempo de ejecución de suite < 30 segundos en entorno local.
- Capacidad de detectar errores comunes antes de llegar a producción (import faltante, JSON inválido, etc.).
- Reporte de resultados enlazado en la bitácora MAP cuando se ejecute la suite.
