# 🤖 Meta-Agente Generador de Agentes AI

Un sistema inteligente que crea agentes AI personalizados automáticamente mediante conversación natural.

## ✨ Características

- **Conversacional**: Describe lo que necesitas en lenguaje natural
- **Inteligente**: Hace preguntas aclaratorias para entender tus necesidades
- **Automático**: Genera código Python funcional listo para usar
- **Flexible**: Soporta diferentes niveles de complejidad (básico, con memoria, equipos)
- **Moderno**: Usa el framework Agno (10,000x más rápido que LangChain)

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar o descargar el proyecto
cd 04-Meta-Agent

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu API key de Anthropic
# ANTHROPIC_API_KEY=tu_api_key_aqui
```

Obtén tu API key en: https://console.anthropic.com/

### 3. Ejecutar

```bash
python main.py
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

## 📁 Estructura del Proyecto

```
04-Meta-Agent/
├── meta_agent.py           # Lógica principal del meta-agente
├── agent_templates.py      # Sistema de plantillas
├── main.py                 # Punto de entrada CLI
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de configuración
├── README.md              # Este archivo
└── generated/             # Agentes generados (creado automáticamente)
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

- **DeepSeek** (DeepSeek): `deepseek-chat` (default), `deepseek-reasoner`
- **Claude** (Anthropic): `claude-sonnet-4-20250514`
- **GPT** (OpenAI): `gpt-4o`, `gpt-4-turbo`
- **Gemini** (Google): `gemini-2.0-flash-exp`

## 💡 Ejemplos de Uso

### Ejemplo 1: Agente de Noticias

```bash
python main.py

> Un agente que busque noticias de tecnología y startups
> Quiero que use búsqueda web
> No necesita memoria
```

Genera: `buscador_de_noticias_agent.py`

### Ejemplo 2: Asistente Financiero

```bash
python main.py

> Necesito un analista de acciones
> Debe usar datos financieros en tiempo real
> Que recuerde mis acciones favoritas
```

Genera: `analista_de_acciones_agent.py` (con memoria)

### Ejemplo 3: Equipo de Investigación

```bash
python main.py

> Un equipo de agentes para investigación académica
> Un miembro busca información, otro analiza, otro escribe
> No necesita memoria
```

Genera: `equipo_de_investigacion_agent.py` (equipo)

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
