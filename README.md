# 🤖 Meta-Agente Generador de Agentes AI

Un sistema completo basado en **Agno v2** con **AgentOS** y **Lantui TUI** que conversa contigo, diseña agentes especializados y genera código listo para ejecutar.

## ✨ Características

- **Conversacional**: Describe lo que necesitas en lenguaje natural
- **Inteligente**: Hace preguntas aclaratorias para entender tus necesidades
- **Automático**: Genera código Python funcional listo para usar
- **Flexible**: Soporta diferentes niveles de complejidad (básico, con memoria, equipos)
- **Moderno**: Usa el framework Agno (10,000x más rápido que LangChain)
- **AgentOS**: API RESTful completa con gestión de sesiones y persistencia
- **Lantui TUI**: Interfaz de terminal moderna estilo Claude Code (Go + Bubble Tea)

## 🚀 Inicio Rápido

### Backend (AgentOS)

1. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno**

   Copia `.env.example` a `.env` y define las claves necesarias:

   ```env
   ANTHROPIC_API_KEY=tu_api_key  # Para Claude
   DEEPSEEK_API_KEY=tu_api_key   # Para DeepSeek (opcional)
   ```

3. **Ejecutar AgentOS**

   ```bash
   python agentos.py
   ```

   El servidor estará disponible en `http://localhost:7777`

### Frontend (Lantui TUI)

1. **Requisitos**: Go 1.21+

2. **Ejecutar Lantui**

   ```bash
   cd lantui
   go mod download
   go run cmd/lantui/main.go
   ```

### CLI Clásica (sin AgentOS)

```bash
python -m src.presentation.cli.main
```

## 📖 Cómo Usar

### Ejemplo de Conversación

```
🤖 Meta-Agente Generador de Agentes AI

¿Qué tipo de agente necesitas?
> Un agente que busque noticias de tecnología

Meta-Agente: ¿Qué herramientas necesita el agente?
a) Búsqueda web (noticias, información general)
b) Datos financieros (acciones, mercados)
c) Otra (especifica)

> a

Meta-Agente: ¿Necesita memoria de conversaciones previas?
> No

✓ Tengo toda la información necesaria

📋 Plan del Agente:
Nombre: Buscador de Noticias Tech
Rol: Buscar noticias de tecnología
Modelo: claude-sonnet-4
Herramientas: duckduckgo
...

✓ Agente generado exitosamente: buscador_de_noticias_tech_agent.py
```

### Tipos de Agentes que Puedes Crear

#### 1. Agente Básico (Nivel 1)
- Agente simple con herramientas
- Sin memoria persistente
- Ideal para tareas puntuales

**Ejemplo**: "Un agente que busque información en internet"

#### 2. Agente con Memoria (Nivel 3)
- Recuerda conversaciones previas
- Storage persistente (SQLite)
- Ideal para asistentes personales

**Ejemplo**: "Un asistente personal que recuerde mis preferencias"

#### 3. Equipo de Agentes (Nivel 4)
- Múltiples agentes colaborando
- Cada uno con especialidad
- Ideal para tareas complejas

**Ejemplo**: "Un equipo de investigación y análisis"

## 🛠️ Herramientas Disponibles

| Herramienta | Descripción | Uso |
|-------------|-------------|-----|
| `duckduckgo` | Búsqueda web | Noticias, información general |
| `yfinance` | Datos financieros | Precios de acciones, análisis |
| `reasoning` | Razonamiento complejo | Análisis, decisiones |
| `python` | Ejecutar código | Cálculos, procesamiento |
| `file` | Manipular archivos | Leer, escribir archivos |

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   Lantui (Go TUI)                       │
│         Terminal UI moderna (Bubble Tea)                │
│    Pantallas: Welcome│Conversation│Plan│Generation      │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/REST (puerto 7777)
┌─────────────────────▼───────────────────────────────────┐
│                  AgentOS (FastAPI)                      │
│                                                         │
│  ┌────────────────────────────────────────────┐        │
│  │   Analyzer Agent  │  Planner Agent         │        │
│  │   (Preguntas)     │  (Crea planes)         │        │
│  └────────────────────────────────────────────┘        │
│                                                         │
│  Storage: SQLite (sesiones, memoria)                   │
│  API: /agents/{id}/chat, /api/meta-agent/generate     │
└─────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Generated Agents (Python)                  │
│           Agentes AI listos para ejecutar               │
└─────────────────────────────────────────────────────────┘
```

### Componentes

- **Lantui (Go)**: Frontend TUI moderno con Bubble Tea
- **AgentOS (Python)**: Backend con API RESTful completa
- **Analyzer Agent**: Analiza solicitudes y hace preguntas
- **Planner Agent**: Crea planes estructurados
- **Generator**: Genera código Python de agentes
- **SQLite Storage**: Persistencia de sesiones y memoria

## 📁 Arquitectura del Código

```
.
├── agentos.py                 # ⭐ AgentOS - Servidor principal
├── lantui/                    # 🎨 Frontend TUI (Go)
│   ├── cmd/lantui/            # Entry point
│   ├── internal/
│   │   ├── ui/                # Componentes Bubble Tea
│   │   ├── client/            # Cliente AgentOS
│   │   └── models/            # Estructuras de datos
│   └── README.md
├── src/
│   ├── application/
│   ├── __init__.py
│   └── services/
│       └── meta_agent.py        # Orquestador del flujo conversacional (Analyzer + Planner)
├── infrastructure/
│   ├── __init__.py
│   └── templates/
│       └── agent_templates.py   # Generación de código (básico, memoria, equipos)
├── domain/
│   └── __init__.py              # Entidades de dominio (extensible)
└── presentation/
    └── cli/
        └── main.py              # Interface de línea de comandos

generated/
├── README.md                    # Guía de la carpeta
└── agents/                      # Ejemplos de agentes generados (versionados)

tools/verify_setup.py            # Script de verificación de entorno
requirements.txt                 # Dependencias (Agno v2 + requests + dotenv + rich)
.env.example                     # Variables de entorno de ejemplo
```

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Requerido
ANTHROPIC_API_KEY=tu_api_key

# Opcional (para usar otros modelos)
OPENAI_API_KEY=tu_api_key
GOOGLE_API_KEY=tu_api_key

# Configuración adicional
LOG_LEVEL=INFO
```

### Modelos Soportados

- **DeepSeek**: `deepseek-chat` (default Analyzer) y `deepseek-reasoner` (Planner y equipos)
- **Agno v2** permite conectar otros modelos (Claude, GPT, Gemini) modificando el plan generado

## 💡 Ejemplos de Uso

### Ejemplo 1: Agente Conversacional con Búsqueda Web

```bash
python generated/agents/asistente_conversacional_con_búsqueda_web_agent.py
```

Incluye memoria persistente (`SqliteDb`) y herramientas DuckDuckGo + Serper.

### Ejemplo 2: Asistente Financiero

```bash
python main.py

> Necesito un analista de acciones
> Debe usar datos financieros en tiempo real
> Que recuerde mis acciones favoritas
```

Genera: `analista_de_acciones_agent.py` (con memoria)

### Ejemplo 3: Equipo de Artículos de IA

```bash
python generated/agents/equipo_de_creación_de_artículos_de_ia_agent.py
```

Tres agentes DeepSeek que colaboran (investigación, redacción y SEO).

## 🧪 Testing y Scripts de Ejemplo

- Instala dependencias de desarrollo:

  ```bash
  pip install -r requirements-dev.txt
  ```

- Ejecuta la suite de tests con cobertura:

  ```bash
  pytest
  ```

- Revisa cobertura detallada:

  ```bash
  coverage report
  ```

- Scripts de ejemplo (ubicados en `tools/`):

  ```bash
  python tools/run_meta_agent_example.py           # Agente básico (web search)
  python tools/run_meta_agent_topic.py             # Exploración de tema IA
  python tools/run_meta_agent_with_memory.py       # Agente con memoria persistente
  python tools/run_meta_agent_team.py              # Equipo colaborativo de agentes
  ```

- Consulta `dics/plan_pruebas_manual.md` para escenarios manuales y `dics/plan_suite_automatizada.md` para el roadmap de testing automatizado.

### Integración Continua

- El workflow `.github/workflows/tests.yml` ejecuta la suite automáticamente en cada push/PR hacia `main` o `master`:

  ```yaml
  - name: Run tests with coverage
    run: |
      pytest
  ```

## 📚 Documentación

### Backend (Python + AgentOS)
- **[agentos.py](./agentos.py)** - Servidor AgentOS principal
- **[src/application/services/meta_agent.py](./src/application/services/meta_agent.py)** - Lógica del Meta-Agente
- **[src/infrastructure/api/meta_routes.py](./src/infrastructure/api/meta_routes.py)** - Rutas custom de API
- **[src/infrastructure/templates/agent_templates.py](./src/infrastructure/templates/agent_templates.py)** - Generación de código

### Frontend (Go + Lantui)
- **[doc-frontend/](./doc-frontend/)** - Documentación completa del TUI
  - [resumen-agentos.md](./doc-frontend/resumen-agentos.md) - ⭐ **EMPIEZA AQUÍ**
  - [setup-inicial.md](./doc-frontend/setup-inicial.md) - Guía de instalación Go
  - [api-contracts-agentos.md](./doc-frontend/api-contracts-agentos.md) - Contratos de API
  - [guia-estilo-go.md](./doc-frontend/guia-estilo-go.md) - Convenciones Go

### API Endpoints

**AgentOS Nativos:**
- `GET /health` - Health check
- `GET /config` - Configuración del OS
- `GET /docs` - Documentación Swagger
- `POST /agents/{agent_id}/chat` - Chat con agentes
- `GET /sessions` - Listar sesiones

**Custom Meta-Agent:**
- `POST /api/meta-agent/generate` - Generar código
- `POST /api/meta-agent/generate-stream` - Con streaming
- `GET /api/meta-agent/generated` - Listar agentes generados

Ver detalles en [http://localhost:7777/docs](http://localhost:7777/docs) cuando AgentOS esté corriendo.

## 🎯 Casos de Uso

- **Búsqueda e Investigación**: Agentes que buscan y analizan información
- **Análisis Financiero**: Seguimiento de mercados y acciones
- **Asistentes Personales**: Con memoria de preferencias y contexto
- **Automatización**: Tareas repetitivas con datos actualizados
- **Equipos Especializados**: Múltiples agentes trabajando juntos

## 🐛 Solución de Problemas

### Error: "ANTHROPIC_API_KEY no configurada"

**Solución**: Copia `.env.example` a `.env` y añade tu API key.

### Error: "ModuleNotFoundError: No module named 'agno'"

**Solución**: Instala las dependencias: `pip install -r requirements.txt`

### El agente generado no funciona

**Checklist**:
1. ¿Instalaste todas las dependencias?
2. ¿Configuraste el archivo .env?
3. ¿El código generado tiene errores de sintaxis?
4. ¿Las herramientas están correctamente importadas?

### Preguntas aclaratorias muy repetitivas

El analyzer_agent a veces necesita contexto. Sé más específico en tu primera descripción:

❌ "Un agente de búsqueda"
✅ "Un agente que busque noticias de tecnología usando búsqueda web, sin memoria"

## 📚 Recursos

- **Agno Framework**: https://docs.agno.com
- **Agno GitHub**: https://github.com/agno-agi/agno
- **Anthropic Claude**: https://www.anthropic.com/claude
- **Documentación del Proyecto**: Ver archivos `proyect_context.md` y `cursor_prompts.md`

## 🤝 Contribuir

Este proyecto está diseñado para ser extensible. Áreas de mejora:

- [ ] Más herramientas Agno
- [ ] Soporte para workflows (Nivel 5)
- [ ] API REST con FastAPI
- [ ] Interfaz web con Gradio
- [ ] Tests unitarios
- [ ] Validación de código generado

## 📝 Notas Técnicas

### Por qué Agno y no LangChain

- **Performance**: ~10,000x más rápido en instantiation
- **Memoria**: ~50x menos uso de memoria
- **API**: Más limpia y menos boilerplate
- **Moderno**: Diseñado para multi-modal y multi-agente

### Arquitectura del Meta-Agente

El sistema usa dos agentes especializados:

1. **Analyzer Agent**: Analiza solicitudes y hace preguntas
2. **Planner Agent**: Crea planes estructurados en JSON

Los planes se validan con Pydantic y se transforman en código mediante templates.

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para crear tus propios agentes.

## 🙋 Soporte

Si encuentras problemas o tienes sugerencias, abre un issue o consulta la documentación completa en `proyect_context.md`.

---

**Hecho con ❤️ usando Agno y Claude AI**
