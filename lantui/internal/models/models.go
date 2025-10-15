package models

import "time"

// ChatRequest representa una solicitud de chat a un agente
type ChatRequest struct {
	Message   string `json:"message"`
	Stream    bool   `json:"stream"`
	SessionID string `json:"session_id,omitempty"`
}

// ChatResponse representa la respuesta de un agente
type ChatResponse struct {
	Content   string    `json:"content"`
	SessionID string    `json:"session_id"`
	Agent     string    `json:"agent"`
	Timestamp time.Time `json:"timestamp"`
}

// AgentPlan representa el plan estructurado de un agente
type AgentPlan struct {
	Nombre          string                   `json:"nombre"`
	Rol             string                   `json:"rol"`
	Modelo          string                   `json:"modelo"`
	Nivel           int                      `json:"nivel"`
	Herramientas    []string                 `json:"herramientas"`
	Instrucciones   []string                 `json:"instrucciones"`
	NecesitaMemoria bool                     `json:"necesita_memoria"`
	EsEquipo        bool                     `json:"es_equipo"`
	MiembrosEquipo  []map[string]interface{} `json:"miembros_equipo,omitempty"`
	EjemploUso      string                   `json:"ejemplo_uso"`
}

// GenerateRequest representa una solicitud de generación de código
type GenerateRequest struct {
	Plan    AgentPlan       `json:"plan"`
	Options GenerateOptions `json:"options"`
}

// GenerateOptions son las opciones para generar código
type GenerateOptions struct {
	IncludeComments bool `json:"include_comments"`
	AddExamples     bool `json:"add_examples"`
	SaveToFile      bool `json:"save_to_file"`
}

// GenerateResponse es la respuesta con el código generado
type GenerateResponse struct {
	Code      string    `json:"code"`
	Plan      AgentPlan `json:"plan"`
	Filename  string    `json:"filename"`
	Filepath  string    `json:"filepath"`
	Lines     int       `json:"lines"`
	SizeBytes int       `json:"size_bytes"`
	CreatedAt string    `json:"created_at"`
}

// Message representa un mensaje en la conversación
type Message struct {
	Role      string    `json:"role"` // "user" o "assistant"
	Content   string    `json:"content"`
	Timestamp time.Time `json:"timestamp"`
}

// Session representa una sesión de conversación
type Session struct {
	SessionID    string    `json:"session_id"`
	AgentID      string    `json:"agent_id"`
	Messages     []Message `json:"messages,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
	MessageCount int       `json:"message_count,omitempty"`
}

// AgentInfo representa información de un agente en el OS
type AgentInfo struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Model       string `json:"model"`
}

// OSConfig representa la configuración del AgentOS
type OSConfig struct {
	OSID        string      `json:"os_id"`
	Description string      `json:"description"`
	Agents      []AgentInfo `json:"agents"`
}

// HealthResponse es la respuesta del health check
type HealthResponse struct {
	Status string `json:"status"`
}

// ErrorResponse es el formato estándar de errores
type ErrorResponse struct {
	Error ErrorDetail `json:"error"`
}

// ErrorDetail contiene detalles del error
type ErrorDetail struct {
	Code    string                 `json:"code"`
	Message string                 `json:"message"`
	Details map[string]interface{} `json:"details,omitempty"`
}
