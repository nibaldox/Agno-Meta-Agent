# Contratos de API - Backend ↔ Frontend

> **Propósito:** Definir interfaces entre Lantui (Go) y AgentOS (Python/Agno)  
> **Versión:** 1.0 Draft  
> **Estado:** 🟡 Propuesta (Pendiente aprobación del equipo backend)  
> **Base:** Agno AgentOS API + extensiones para Meta-Agente

---

## 🎯 Objetivo

Establecer contratos claros que permitan:
1. **Desarrollo paralelo** sin bloqueos
2. **Integración nativa** con Agno AgentOS
3. **Mocking** efectivo para testing
4. **Extensibilidad** para funcionalidades custom del Meta-Agente

---

## 🏗️ Arquitectura de Comunicación

### AgentOS como Backend

```
┌─────────────┐                      ┌──────────────────┐
│   Lantui    │     AgentOS API      │   AgentOS        │
│   (Go TUI)  │ ◄─────────────────► │   (FastAPI)      │
│             │    HTTP/REST         │                  │
│             │                       │  ├─ Meta-Agent  │
│             │                       │  ├─ Agents      │
│             │                       │  ├─ Sessions    │
│             │                       │  └─ Knowledge   │
└─────────────┘                       └──────────────────┘
```

**Decisión:** Usar AgentOS como backend principal, extendiendo con endpoints custom para generación de agentes

### Ventajas de AgentOS

✅ **API RESTful completa** ya incluida  
✅ **Gestión de sesiones** automática  
✅ **Storage y memoria** configurables  
✅ **Multi-agente** soporte nativo  
✅ **Control Plane web** opcional  
✅ **Autenticación** con bearer tokens

---

## 📋 AgentOS API Estándar

### Endpoints Nativos de AgentOS

Lantui usará directamente estos endpoints de AgentOS:

#### 1. Health Check

**Endpoint:** `GET /health`

**Propósito:** Verificar estado del AgentOS

**Response:**
```json
{
  "status": "ok"
}
```

#### 2. Configuración del OS

**Endpoint:** `GET /config`

**Propósito:** Obtener configuración completa del AgentOS

**Response:**
```json
{
  "os_id": "meta-agent-os",
  "description": "Meta-Agente Generador con AgentOS",
  "databases": [...],
  "agents": [
    {
      "id": "analyzer_agent",
      "name": "Analyzer Agent",
      "description": "Analiza solicitudes de usuarios"
    },
    {
      "id": "planner_agent", 
      "name": "Planner Agent",
      "description": "Crea planes estructurados"
    }
  ]
}
```

#### 3. Chat con Agente (AgentOS API)

**Endpoint:** `POST /agents/{agent_id}/chat`

**Propósito:** Interactuar con agentes del sistema (analyzer, planner)

**Request:**
```json
{
  "message": "Quiero crear un agente de búsqueda",
  "stream": false,
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "content": "¿Qué tipo de búsqueda te interesa?...",
  "session_id": "generated-session-id",
  "agent": "analyzer_agent"
}
```

#### 4. Sesiones (AgentOS API)

**Endpoint:** `GET /sessions`

**Propósito:** Listar sesiones de conversación

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "uuid-1234",
      "agent_id": "analyzer_agent",
      "created_at": "2025-10-14T12:00:00Z",
      "updated_at": "2025-10-14T12:05:00Z",
      "message_count": 5
    }
  ]
}
```

---

## 🔧 Endpoints Custom para Meta-Agente

Extensiones específicas para funcionalidad de generación de agentes (agregadas al AgentOS):

### 1. Generar Plan de Agente

**Endpoint:** `POST /api/meta-agent/generate-plan`

**Propósito:** Analizar solicitud inicial del usuario y determinar si se necesitan preguntas aclaratorias

**Request:**
```json
{
  "request": "Quiero crear un agente que busque noticias sobre IA"
}
```

**Response:**
```json
{
  "needs_clarification": true,
  "questions": [
    "¿Qué fuentes de noticias prefieres?",
    "¿Con qué frecuencia quieres que busque?",
    "¿Algún tema específico dentro de IA?"
  ],
  "confidence": 0.85
}
```

**Go Models:**
```go
type AnalyzeRequest struct {
    Request string `json:"request"`
}

type AnalysisResponse struct {
    NeedsClarification bool     `json:"needs_clarification"`
    Questions          []string `json:"questions"`
    Confidence         float64  `json:"confidence"`
}
```

**Python Implementation:**
```python
class AnalyzeRequest(BaseModel):
    request: str

class AnalysisResponse(BaseModel):
    needs_clarification: bool
    questions: List[str]
    confidence: float

@app.post("/api/v1/analyze")
async def analyze_request(req: AnalyzeRequest) -> AnalysisResponse:
    # Usar analyzer_agent
    result = analyzer_agent.run(req.request)
    return AnalysisResponse(...)
```

---

### 3. Process Answer

**Endpoint:** `POST /api/v1/conversation/answer`

**Propósito:** Enviar respuesta del usuario a pregunta aclaratoria

**Request:**
```json
{
  "conversation_id": "uuid-1234",
  "question": "¿Qué fuentes de noticias prefieres?",
  "answer": "TechCrunch y Ars Technica"
}
```

**Response:**
```json
{
  "conversation_id": "uuid-1234",
  "continue": true,
  "next_question": "¿Con qué frecuencia quieres que busque?",
  "progress": 0.33
}
```

**Go Models:**
```go
type AnswerRequest struct {
    ConversationID string `json:"conversation_id"`
    Question       string `json:"question"`
    Answer         string `json:"answer"`
}

type ConversationResponse struct {
    ConversationID string  `json:"conversation_id"`
    Continue       bool    `json:"continue"`
    NextQuestion   string  `json:"next_question,omitempty"`
    Progress       float64 `json:"progress"`
}
```

---

### 4. Create Plan

**Endpoint:** `POST /api/v1/plan/create`

**Propósito:** Generar plan estructurado del agente basado en la conversación

**Request:**
```json
{
  "conversation_id": "uuid-1234",
  "messages": [
    {"role": "user", "content": "Crear agente de noticias IA"},
    {"role": "assistant", "content": "¿Qué fuentes?"},
    {"role": "user", "content": "TechCrunch"}
  ]
}
```

**Response:**
```json
{
  "plan": {
    "nombre": "Buscador de Noticias IA",
    "rol": "Buscar y resumir noticias sobre inteligencia artificial",
    "modelo": "claude-sonnet-4-20250514",
    "nivel": 1,
    "herramientas": ["duckduckgo", "newspaper"],
    "instrucciones": [
      "Buscar noticias recientes sobre IA",
      "Filtrar por fuentes confiables",
      "Generar resumen estructurado"
    ],
    "ejemplo_uso": "Busca noticias sobre GPT-5",
    "descripcion": "Agente especializado en buscar noticias tech"
  },
  "estimated_lines": 120,
  "estimated_time_seconds": 15
}
```

**Go Models:**
```go
type Message struct {
    Role    string `json:"role"`
    Content string `json:"content"`
}

type CreatePlanRequest struct {
    ConversationID string    `json:"conversation_id"`
    Messages       []Message `json:"messages"`
}

type AgentPlan struct {
    Nombre              string   `json:"nombre"`
    Rol                 string   `json:"rol"`
    Modelo              string   `json:"modelo"`
    Nivel               int      `json:"nivel"`
    Herramientas        []string `json:"herramientas"`
    Instrucciones       []string `json:"instrucciones"`
    EjemploUso          string   `json:"ejemplo_uso"`
    Descripcion         string   `json:"descripcion"`
}

type PlanResponse struct {
    Plan                   AgentPlan `json:"plan"`
    EstimatedLines         int       `json:"estimated_lines"`
    EstimatedTimeSeconds   int       `json:"estimated_time_seconds"`
}
```

**Python Implementation:**
```python
from src.application.services.meta_agent import AgentPlan

@app.post("/api/v1/plan/create")
async def create_plan(req: CreatePlanRequest) -> PlanResponse:
    # Usar planner_agent
    plan = planner_agent.run(req.messages)
    return PlanResponse(
        plan=plan,
        estimated_lines=estimate_lines(plan),
        estimated_time_seconds=15
    )
```

---

### 5. Generate Code

**Endpoint:** `POST /api/v1/code/generate`

**Propósito:** Generar código Python del agente basado en el plan

**Request:**
```json
{
  "plan": {
    "nombre": "Buscador de Noticias IA",
    "rol": "...",
    ...
  },
  "options": {
    "include_comments": true,
    "add_examples": true
  }
}
```

**Response (No streaming):**
```json
{
  "code": "\"\"\"\\nAgente para buscar noticias...\\n\"\"\"\\n\\nfrom agno...",
  "filename": "buscador_de_noticias_ia_agent.py",
  "lines": 125,
  "size_bytes": 3840
}
```

**Go Models:**
```go
type GenerateRequest struct {
    Plan    AgentPlan       `json:"plan"`
    Options GenerateOptions `json:"options"`
}

type GenerateOptions struct {
    IncludeComments bool `json:"include_comments"`
    AddExamples     bool `json:"add_examples"`
}

type GenerateResponse struct {
    Code      string `json:"code"`
    Filename  string `json:"filename"`
    Lines     int    `json:"lines"`
    SizeBytes int    `json:"size_bytes"`
}
```

---

### 6. Generate Code (Streaming)

**Endpoint:** `POST /api/v1/code/generate-stream`

**Propósito:** Generar código con streaming para feedback en tiempo real

**Request:** Igual que `/generate`

**Response (SSE - Server-Sent Events):**
```
data: {"type": "progress", "step": "imports", "percentage": 10}

data: {"type": "code", "chunk": "\"\"\"\\nAgente para..."}

data: {"type": "progress", "step": "tools", "percentage": 40}

data: {"type": "code", "chunk": "\\nfrom agno.tools..."}

data: {"type": "progress", "step": "complete", "percentage": 100}

data: {"type": "done", "filename": "agent.py", "lines": 125}
```

**Go Client:**
```go
type StreamEvent struct {
    Type       string `json:"type"` // "progress", "code", "done", "error"
    Step       string `json:"step,omitempty"`
    Percentage int    `json:"percentage,omitempty"`
    Chunk      string `json:"chunk,omitempty"`
    Filename   string `json:"filename,omitempty"`
    Lines      int    `json:"lines,omitempty"`
}

func (c *Client) GenerateCodeStream(ctx context.Context, req GenerateRequest) (<-chan StreamEvent, error) {
    // Implementación con SSE
}
```

**Python Implementation:**
```python
from fastapi.responses import StreamingResponse

@app.post("/api/v1/code/generate-stream")
async def generate_code_stream(req: GenerateRequest):
    async def event_generator():
        yield f"data: {json.dumps({'type': 'progress', 'step': 'start'})}\n\n"
        
        # Generar código en chunks
        code = generate_code(req.plan)
        for i, chunk in enumerate(split_code(code, chunks=10)):
            yield f"data: {json.dumps({'type': 'code', 'chunk': chunk})}\n\n"
            yield f"data: {json.dumps({'type': 'progress', 'percentage': (i+1)*10})}\n\n"
            await asyncio.sleep(0.1)  # Simular trabajo
        
        yield f"data: {json.dumps({'type': 'done', 'filename': 'agent.py'})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

---

## 🔐 Autenticación y Seguridad

### Fase 1 (MVP): Sin autenticación
- Backend corre localmente
- Frontend se conecta a `localhost:8000`
- Solo para desarrollo/uso personal

### Fase 2 (Futuro): API Key
```http
Authorization: Bearer <API_KEY>
```

### Fase 3 (Futuro): OAuth/JWT
- Multi-usuario
- Sesiones persistentes
- Rate limiting

---

## 🚨 Manejo de Errores

### Formato Estándar de Error

Todos los endpoints retornan errores en formato consistente:

```json
{
  "error": {
    "code": "INVALID_PLAN",
    "message": "El nivel del agente debe ser entre 1 y 5",
    "details": {
      "field": "nivel",
      "value": 10,
      "constraint": "1-5"
    }
  }
}
```

**Go Model:**
```go
type ErrorResponse struct {
    Error ErrorDetail `json:"error"`
}

type ErrorDetail struct {
    Code    string                 `json:"code"`
    Message string                 `json:"message"`
    Details map[string]interface{} `json:"details,omitempty"`
}
```

### Códigos de Error

| Código | HTTP Status | Descripción |
|--------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Request malformado |
| `INVALID_PLAN` | 400 | Plan no válido |
| `CONVERSATION_NOT_FOUND` | 404 | ID de conversación no existe |
| `GENERATION_FAILED` | 500 | Error al generar código |
| `INTERNAL_ERROR` | 500 | Error interno del servidor |
| `SERVICE_UNAVAILABLE` | 503 | Servicio temporalmente no disponible |

---

## 📊 Timeouts y Límites

### Timeouts Recomendados

```go
const (
    HealthCheckTimeout    = 5 * time.Second
    AnalyzeTimeout        = 30 * time.Second
    ConversationTimeout   = 30 * time.Second
    CreatePlanTimeout     = 60 * time.Second
    GenerateCodeTimeout   = 120 * time.Second
)
```

### Rate Limits (Futuro)

- `analyze`: 10 requests/min por cliente
- `plan/create`: 5 requests/min por cliente
- `code/generate`: 3 requests/min por cliente

---

## 🧪 Testing de Integración

### Mock Server (Para Frontend Development)

```go
// internal/client/mock_client.go
type MockClient struct {
    Delay time.Duration
}

func (m *MockClient) CreatePlan(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error) {
    time.Sleep(m.Delay)
    return &PlanResponse{
        Plan: AgentPlan{
            Nombre:        "Mock Agent",
            Rol:           "Testing purposes",
            Modelo:        "mock-model",
            Nivel:         1,
            Herramientas:  []string{"mock-tool"},
            Instrucciones: []string{"Mock instruction"},
        },
        EstimatedLines:       100,
        EstimatedTimeSeconds: 10,
    }, nil
}
```

### Test Fixtures

```go
// testdata/requests/analyze.json
{
  "request": "Crear un agente de búsqueda"
}

// testdata/responses/analyze.json
{
  "needs_clarification": true,
  "questions": ["¿Qué tipo de búsqueda?"],
  "confidence": 0.9
}
```

---

## 📝 Changelog de Contratos

### v1.0.0 (Draft - Octubre 2025)
- ✅ Definición inicial de endpoints
- ✅ Modelos de datos básicos
- ✅ Formato de errores
- ⏳ Pendiente: Aprobación backend team

### v1.1.0 (Planeado)
- Streaming mejorado con progreso detallado
- Soporte para cancelación de generación
- Historial de conversaciones

### v2.0.0 (Futuro)
- Migración a gRPC
- Autenticación
- Multi-tenancy

---

## 🤝 Proceso de Cambio de Contratos

1. **Propuesta:** Crear issue describiendo cambio necesario
2. **Discusión:** Review con ambos equipos (Go + Python)
3. **Aprobación:** Consenso en arquitectura
4. **Implementación:**
   - Backend implementa primero
   - Frontend adapta cliente
5. **Testing:** Integration tests end-to-end
6. **Documentación:** Actualizar este archivo
7. **Release:** Bump de versión semántica

---

## 📚 Recursos

### Implementación Python (Backend)

```bash
# Crear módulo API
src/infrastructure/api/
├── __init__.py
├── server.py          # FastAPI app
├── routes.py          # Endpoints
├── models.py          # Pydantic models
└── middleware.py      # CORS, logging, etc.
```

### Implementación Go (Frontend)

```bash
# Cliente HTTP
internal/client/
├── client.go          # Interface
├── http_client.go     # Implementación
├── mock_client.go     # Mock
└── models.go          # Structs
```

---

## ✅ Checklist de Integración

Backend (Python):
- [ ] Crear módulo `src/infrastructure/api/`
- [ ] Implementar endpoints básicos
- [ ] Añadir modelos Pydantic
- [ ] Setup CORS para desarrollo local
- [ ] Documentación OpenAPI (Swagger)
- [ ] Tests de endpoints

Frontend (Go):
- [ ] Crear interface `MetaAgentClient`
- [ ] Implementar `HTTPClient`
- [ ] Implementar `MockClient` para testing
- [ ] Añadir integration tests
- [ ] Manejo de errores y retry logic

---

**Última actualización:** Octubre 14, 2025  
**Estado:** 🟡 Draft  
**Aprobación pendiente:** Backend Team  
**Próxima revisión:** Milestone 1 (Setup inicial)

