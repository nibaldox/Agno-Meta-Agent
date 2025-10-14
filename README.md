# 🤖 Meta-Agente Generador de Agentes AI

Un sistema modular basado en **Agno v2** que conversa contigo, diseña agentes especializados y genera código listo para ejecutar.

## ✨ Características

- **Conversacional**: Describe lo que necesitas en lenguaje natural
- **Inteligente**: Hace preguntas aclaratorias para entender tus necesidades
- **Automático**: Genera código Python funcional listo para usar
- **Flexible**: Soporta diferentes niveles de complejidad (básico, con memoria, equipos)
- **Moderno**: Usa el framework Agno (10,000x más rápido que LangChain)

## 🚀 Inicio Rápido

1. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno**

   Copia `.env.example` a `.env` y define las claves necesarias:

   ```env
   DEEPSEEK_API_KEY=tu_api_key
   SERPER_API_KEY=tu_api_key   # solo si usas la herramienta Serper
   ```

3. **Ejecutar interfaz CLI**

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

## 📁 Arquitectura Limpia

```
src/
├── application/
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
