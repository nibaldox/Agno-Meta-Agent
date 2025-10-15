package client

import (
	"context"
	"fmt"
	"time"

	"github.com/tuorg/meta-agent/lantui/internal/models"
)

// MockClient es un cliente mock para desarrollo sin backend
type MockClient struct {
	Delay        time.Duration
	sessionCount int
}

// NewMockClient crea un nuevo cliente mock
func NewMockClient() *MockClient {
	return &MockClient{
		Delay:        200 * time.Millisecond,
		sessionCount: 0,
	}
}

// Health verifica el estado del AgentOS
func (m *MockClient) Health(ctx context.Context) error {
	time.Sleep(m.Delay)
	return nil
}

// GetConfig obtiene la configuración del OS
func (m *MockClient) GetConfig(ctx context.Context) (*models.OSConfig, error) {
	time.Sleep(m.Delay)

	return &models.OSConfig{
		OSID:        "meta-agent-os-v1",
		Description: "Meta-Agente Generador con AgentOS",
		Agents: []models.AgentInfo{
			{
				ID:          "analyzer_agent",
				Name:        "Analyzer Agent",
				Description: "Analiza solicitudes y genera preguntas aclaratorias",
				Model:       "deepseek-chat",
			},
			{
				ID:          "planner_agent",
				Name:        "Planner Agent",
				Description: "Crea planes estructurados de agentes",
				Model:       "deepseek-reasoner",
			},
		},
	}, nil
}

// Chat envía un mensaje a un agente (mock)
func (m *MockClient) Chat(ctx context.Context, agentID string, req models.ChatRequest) (*models.ChatResponse, error) {
	time.Sleep(m.Delay)

	// Generar respuesta mock según el agente
	var content string
	switch agentID {
	case "analyzer_agent":
		if m.sessionCount == 0 {
			content = "¡Perfecto! Voy a ayudarte a crear ese agente.\n\n¿Qué herramientas necesita el agente?\n\na) Búsqueda web (noticias, información general)\nb) Datos financieros (acciones, mercados)\nc) Análisis de archivos\nd) Ejecución de código Python\ne) Otra (especifica)"
		} else if m.sessionCount == 1 {
			content = "Excelente elección.\n\n¿El agente necesita recordar conversaciones previas (memoria persistente)?\n\na) Sí, necesita memoria\nb) No, cada conversación es independiente"
		} else {
			content = "INFO_COMPLETA\n\nTengo toda la información necesaria para crear tu agente."
		}
		m.sessionCount++

	case "planner_agent":
		content = "Plan creado exitosamente"

	default:
		content = "Respuesta mock para: " + req.Message
	}

	sessionID := req.SessionID
	if sessionID == "" {
		sessionID = fmt.Sprintf("mock-session-%d", time.Now().Unix())
	}

	return &models.ChatResponse{
		Content:   content,
		SessionID: sessionID,
		Agent:     agentID,
		Timestamp: time.Now(),
	}, nil
}

// GetSession obtiene una sesión por ID (mock)
func (m *MockClient) GetSession(ctx context.Context, sessionID string) (*models.Session, error) {
	time.Sleep(m.Delay)

	return &models.Session{
		SessionID: sessionID,
		AgentID:   "analyzer_agent",
		Messages: []models.Message{
			{
				Role:      "user",
				Content:   "Crear un agente de búsqueda de noticias",
				Timestamp: time.Now().Add(-5 * time.Minute),
			},
			{
				Role:      "assistant",
				Content:   "¿Qué herramientas necesita?",
				Timestamp: time.Now().Add(-4 * time.Minute),
			},
		},
		CreatedAt:    time.Now().Add(-5 * time.Minute),
		UpdatedAt:    time.Now(),
		MessageCount: 2,
	}, nil
}

// GenerateAgent genera el código de un agente (mock)
func (m *MockClient) GenerateAgent(ctx context.Context, req models.GenerateRequest) (*models.GenerateResponse, error) {
	time.Sleep(m.Delay * 3) // Simular trabajo más pesado

	mockCode := fmt.Sprintf(`"""
%s - Agente AI generado automáticamente.

Rol: %s
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek

def main():
    agent = Agent(
        name="%s",
        role="%s",
        model=DeepSeek(id="%s"),
        markdown=True,
    )
    
    agent.print_response("Hola, ¿cómo puedo ayudarte?", stream=True)

if __name__ == "__main__":
    main()
`, req.Plan.Nombre, req.Plan.Rol, req.Plan.Nombre, req.Plan.Rol, req.Plan.Modelo)

	return &models.GenerateResponse{
		Code:      mockCode,
		Plan:      req.Plan,
		Filename:  fmt.Sprintf("%s_agent.py", req.Plan.Nombre),
		Filepath:  fmt.Sprintf("generated/agents/%s_agent.py", req.Plan.Nombre),
		Lines:     len(mockCode) / 50, // Aprox
		SizeBytes: len(mockCode),
		CreatedAt: time.Now().Format(time.RFC3339),
	}, nil
}
