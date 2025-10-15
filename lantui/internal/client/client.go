package client

import (
	"context"

	"github.com/tuorg/meta-agent/lantui/internal/models"
)

// AgentOSClient es la interfaz para interactuar con AgentOS
type AgentOSClient interface {
	// Health verifica el estado del AgentOS
	Health(ctx context.Context) error

	// GetConfig obtiene la configuración del OS
	GetConfig(ctx context.Context) (*models.OSConfig, error)

	// Chat envía un mensaje a un agente
	Chat(ctx context.Context, agentID string, req models.ChatRequest) (*models.ChatResponse, error)

	// GetSession obtiene una sesión por ID
	GetSession(ctx context.Context, sessionID string) (*models.Session, error)

	// GenerateAgent genera el código de un agente
	GenerateAgent(ctx context.Context, req models.GenerateRequest) (*models.GenerateResponse, error)
}
