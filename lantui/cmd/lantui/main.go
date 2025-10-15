package main

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// Versión de Lantui
const version = "1.0.0-dev"

// Model es el estado de la aplicación Bubble Tea
type model struct {
	ready      bool
	agentosURL string
	width      int
	height     int
}

// Init inicializa la aplicación
func (m model) Init() tea.Cmd {
	return nil
}

// Update maneja los mensajes y actualiza el estado
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c", "esc":
			return m, tea.Quit
		case "enter":
			m.ready = true
		}

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
	}

	return m, nil
}

// View renderiza la UI
func (m model) View() string {
	if !m.ready {
		return welcomeView(m)
	}
	return runningView(m)
}

// welcomeView renderiza la pantalla de bienvenida
func welcomeView(m model) string {
	// Estilos
	titleStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("#88C0D0")).
		Bold(true).
		Padding(0, 1)

	subtitleStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("#B48EAD")).
		Italic(true)

	boxStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#434C5E")).
		Padding(1, 2).
		Width(60)

	promptStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("#A3BE8C"))

	dimStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("#4C566A"))

	// Contenido
	title := titleStyle.Render("🤖  Meta-Agente Generador")
	subtitle := subtitleStyle.Render("Terminal UI para crear agentes AI personalizados")

	info := lipgloss.JoinVertical(
		lipgloss.Left,
		"",
		"Crea agentes AI de forma conversacional",
		"✨ Interfaz moderna y fluida",
		"🚀 Powered by Agno Framework",
		"",
	)

	status := dimStyle.Render(fmt.Sprintf("AgentOS: %s", m.agentosURL))

	prompt := promptStyle.Render("[Presiona ENTER para comenzar]")
	quit := dimStyle.Render("[Q para salir]")

	content := lipgloss.JoinVertical(
		lipgloss.Center,
		title,
		subtitle,
		info,
		status,
		"",
		prompt,
		quit,
	)

	box := boxStyle.Render(content)

	// Centrar en la pantalla
	return lipgloss.Place(
		m.width,
		m.height,
		lipgloss.Center,
		lipgloss.Center,
		box,
	)
}

// runningView muestra que la app está corriendo
func runningView(m model) string {
	style := lipgloss.NewStyle().
		Foreground(lipgloss.Color("#A3BE8C")).
		Bold(true).
		Padding(1, 2)

	content := lipgloss.JoinVertical(
		lipgloss.Left,
		"✓ Lantui está funcionando!",
		"",
		"🚧 Desarrollo en progreso...",
		"",
		"Próximas pantallas:",
		"  • Conversation Screen",
		"  • Plan Review Screen",
		"  • Generation Progress",
		"  • Success Screen",
		"",
		"[Presiona Q para salir]",
	)

	box := style.Render(content)

	return lipgloss.Place(
		m.width,
		m.height,
		lipgloss.Center,
		lipgloss.Center,
		box,
	)
}

func main() {
	// Configuración inicial
	agentosURL := os.Getenv("AGENTOS_URL")
	if agentosURL == "" {
		agentosURL = "http://localhost:7777"
	}

	// Crear modelo inicial
	m := model{
		ready:      false,
		agentosURL: agentosURL,
		width:      80,
		height:     24,
	}

	// Iniciar programa Bubble Tea
	p := tea.NewProgram(
		m,
		tea.WithAltScreen(),       // Usar pantalla alternativa
		tea.WithMouseCellMotion(), // Soporte para mouse
	)

	// Ejecutar
	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}
