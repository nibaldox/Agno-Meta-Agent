# ✅ Plan de Pruebas Manuales

## 1. Objetivo

Asegurar que el meta-agente genere agentes funcionales siguiendo el flujo interactivo completo y que el código resultante sea ejecutable con las configuraciones soportadas.

## 2. Alcance

- Flujo `interactive_creation()` desde CLI.
- Generación de agentes de Nivel 1 (básico), Nivel 3 (con memoria) y Nivel 4 (equipo).
- Validación de herramientas disponibles: `duckduckgo`, `yfinance`, `reasoning`, `python`, `file`.
- Persistencia en `generated/agents/` y verificación de ejecución básica.

## 3. Preparación

- Dependencias instaladas con `pip install -r requirements.txt`.
- Archivo `.env` configurado con claves necesarias (Anthropic, DeepSeek, etc.).
- Limpiar carpeta `generated/agents/` o identificar agentes existentes para evitar confusión.
- Activar entorno virtual (`venv\Scripts\activate` en Windows).

## 4. Escenarios de Prueba

| ID | Escenario | Pasos | Resultado Esperado |
|----|-----------|-------|--------------------|
| M-01 | Flujo CLI básico | Ejecutar `python -m src.presentation.cli.main`, describir agente sencillo sin memoria, responder preguntas hasta confirmar | Archivo generado en `generated/agents/`, sin errores en consola |
| M-02 | Preguntas aclaratorias | Proporcionar descripción ambigua para forzar preguntas adicionales y confirmar detección de `INFO_COMPLETA` | Analyzer formula preguntas contextuales, se rompe el loop al tener información suficiente |
| M-03 | Agente con memoria | Solicitar agente con memoria persistente; validar creación de `SqliteAgentStorage` y archivo SQLite | Código contiene configuración de memoria y almacenamiento, ejecución crea/usa `agents_memory.sqlite` |
| M-04 | Equipo de agentes | Pedir equipo colaborativo; validar uso de `Team` en código generado | Archivo contiene estructura de equipo y modelos adecuados |
| M-05 | Selección de herramientas | Solicitar agente que use cada herramienta soportada en combinaciones diferentes | Imports y inicializaciones correctas para cada herramienta |
| M-06 | Reintento de plan | Simular error intencional (editar prompt para plan inválido) y verificar manejo de errores | Mensaje claro en consola indicando fallo al crear plan |

## 5. Criterios de Aceptación

- Ningún escenario produce excepciones no manejadas.
- Código generado compila y corre sin errores sintácticos (`python archivo.py`).
- Los agentes con memoria y equipos incluyen configuraciones correctas de Agno.
- Las herramientas seleccionadas aparecen en imports y listas de configuración del agente.
- Conversación CLI mantiene mensajes estilizados con Rich y flujo amigable.

## 6. Registro de Resultados

Registrar en `dics/bitacora_map.md` la fecha, escenarios ejecutados, resultado (OK/KO) y observaciones. Adjuntar logs de consola si se detectan anomalías.

## 7. Próximos Pasos

- Automatizar escenarios clave en la futura suite (ver `dics/plan_suite_automatizada.md`).
- Añadir pruebas específicas para nuevas herramientas o tipos de agentes conforme se incorporen.
- Considerar checklist previo/posterior a generación (validar entorno, limpiar archivos temporales).

