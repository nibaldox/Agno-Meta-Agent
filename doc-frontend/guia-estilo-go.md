# Guía de Estilo y Mejores Prácticas - Lantui

> **Propósito:** Mantener código consistente, legible y mantenible en el proyecto Lantui  
> **Basado en:** Go Style Guide, Effective Go, Charm Style Guide

---

## 🎯 Principios Generales

1. **Simplicidad sobre Complejidad:** Preferir soluciones directas
2. **Legibilidad sobre Brevedad:** El código se lee más veces de las que se escribe
3. **Convenciones Go Estándar:** Seguir idioms de la comunidad
4. **Performance con Propósito:** Optimizar solo cuando sea necesario y medible
5. **Error Handling Explícito:** Nunca ignorar errores silenciosamente

---

## 📝 Nomenclatura

### Archivos y Paquetes

```go
// ✅ CORRECTO: snake_case para archivos
welcome_screen.go
agent_plan.go
http_client.go

// ❌ INCORRECTO: camelCase o PascalCase
welcomeScreen.go
AgentPlan.go
HTTPClient.go

// ✅ CORRECTO: nombres de paquetes cortos, descriptivos
package ui
package client
package models

// ❌ INCORRECTO: nombres largos o redundantes
package user_interface
package meta_agent_client
package data_models
```

### Variables y Funciones

```go
// ✅ CORRECTO: camelCase para variables y funciones privadas
var currentState string
func processRequest() {}

// ✅ CORRECTO: PascalCase para exportadas
var DefaultTheme Theme
func NewClient() *Client {}

// ✅ CORRECTO: acrónimos en mayúscula al inicio
type HTTPClient struct {}
type URLParser struct {}

// ❌ INCORRECTO: acrónimos con capitalización mixta
type HttpClient struct {} // debe ser HTTPClient
type UrlParser struct {}  // debe ser URLParser

// ✅ CORRECTO: nombres descriptivos
var userInputBuffer strings.Builder
var maxRetryAttempts = 3

// ❌ INCORRECTO: nombres crípticos
var buf strings.Builder  // muy genérico
var n = 3                // no descriptivo
```

### Constantes

```go
// ✅ CORRECTO: PascalCase para exportadas
const DefaultTimeout = 30 * time.Second
const MaxRetries = 5

// ✅ CORRECTO: camelCase para privadas
const bufferSize = 1024
const defaultPort = 8000

// ✅ CORRECTO: grupos con iota
const (
    StateWelcome = iota
    StateConversation
    StatePlanReview
    StateGeneration
)
```

### Interfaces

```go
// ✅ CORRECTO: nombre + "er" para interfaces de un método
type Runner interface {
    Run() error
}

type Reader interface {
    Read(p []byte) (n int, err error)
}

// ✅ CORRECTO: nombres descriptivos para múltiples métodos
type MetaAgentClient interface {
    CreatePlan(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error)
    GenerateCode(ctx context.Context, plan AgentPlan) (string, error)
}

// ❌ INCORRECTO: sufijo "Interface" redundante
type ClientInterface interface {} // solo "Client"
```

---

## 🏗️ Estructura de Código

### Orden de Declaraciones en Archivo

```go
// 1. Package declaration
package screens

// 2. Imports (agrupados)
import (
    // Standard library
    "context"
    "fmt"
    "time"

    // Third-party
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"

    // Local
    "github.com/tuorg/meta-agent/lantui/internal/models"
    "github.com/tuorg/meta-agent/lantui/internal/ui/styles"
)

// 3. Constants
const (
    maxInputLength = 500
    defaultPrompt  = "Escribe tu mensaje..."
)

// 4. Variables (evitar globales cuando sea posible)
var (
    defaultStyle = lipgloss.NewStyle().Padding(1, 2)
)

// 5. Types
type ConversationScreen struct {
    messages []models.Message
    input    string
}

// 6. Constructor
func NewConversationScreen() ConversationScreen {
    return ConversationScreen{
        messages: make([]models.Message, 0),
    }
}

// 7. Methods (receiver methods)
func (c *ConversationScreen) AddMessage(msg models.Message) {
    c.messages = append(c.messages, msg)
}

// 8. Functions
func formatMessage(msg models.Message) string {
    return fmt.Sprintf("[%s] %s", msg.Role, msg.Content)
}

// 9. Helper functions (private)
func parseInput(input string) (string, error) {
    // ...
}
```

### Organización de Structs

```go
// ✅ CORRECTO: campos exportados primero, ordenados lógicamente
type AgentPlan struct {
    // Identificación
    Nombre      string
    Rol         string
    
    // Configuración
    Modelo       string
    Nivel        int
    Herramientas []string
    
    // Detalles
    Instrucciones []string
    EjemploUso    string
    Descripcion   string
    
    // Metadata (privados al final)
    createdAt time.Time
    validated bool
}

// ✅ CORRECTO: usar tags para serialización
type PlanResponse struct {
    Plan                 AgentPlan `json:"plan"`
    EstimatedLines       int       `json:"estimated_lines"`
    EstimatedTimeSeconds int       `json:"estimated_time_seconds"`
}
```

---

## 🎨 Bubble Tea Patterns

### Model Structure

```go
// ✅ CORRECTO: separar estado, vista y lógica
type welcomeModel struct {
    // State
    ready   bool
    loading bool
    err     error
    
    // UI components
    spinner spinner.Model
    
    // Dependencies
    client client.MetaAgentClient
}

// Init: comandos iniciales
func (m welcomeModel) Init() tea.Cmd {
    return tea.Batch(
        m.spinner.Tick,
        checkBackendConnection(),
    )
}

// Update: manejo de mensajes
func (m welcomeModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        return m.handleKeyPress(msg)
    
    case backendStatusMsg:
        return m.handleBackendStatus(msg)
    
    case spinner.TickMsg:
        var cmd tea.Cmd
        m.spinner, cmd = m.spinner.Update(msg)
        return m, cmd
    }
    
    return m, nil
}

// View: renderizado puro (no side effects)
func (m welcomeModel) View() string {
    if m.loading {
        return m.renderLoading()
    }
    if m.err != nil {
        return m.renderError()
    }
    return m.renderWelcome()
}

// ✅ CORRECTO: extraer sub-renders
func (m welcomeModel) renderWelcome() string {
    title := styles.TitleStyle.Render("🤖 Meta-Agente")
    subtitle := styles.SubtitleStyle.Render("Generador de Agentes AI")
    prompt := styles.PromptStyle.Render("[Presiona ENTER para comenzar]")
    
    return lipgloss.JoinVertical(
        lipgloss.Center,
        title,
        subtitle,
        "",
        prompt,
    )
}

// ✅ CORRECTO: separar handlers por tipo de mensaje
func (m welcomeModel) handleKeyPress(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
    switch msg.String() {
    case "enter":
        return m, startConversation
    case "q", "ctrl+c":
        return m, tea.Quit
    default:
        return m, nil
    }
}
```

### Commands y Messages

```go
// ✅ CORRECTO: definir messages como types
type (
    // Mensajes de entrada
    backendStatusMsg struct {
        available bool
        version   string
    }
    
    // Mensajes de progreso
    generationProgressMsg struct {
        percentage int
        step       string
    }
    
    // Mensajes de resultado
    codeGeneratedMsg struct {
        code     string
        filename string
    }
    
    // Mensajes de error
    errorMsg struct{ err error }
)

// ✅ CORRECTO: commands retornan tea.Cmd
func checkBackendConnection() tea.Cmd {
    return func() tea.Msg {
        // Lógica async aquí
        status, err := client.HealthCheck()
        if err != nil {
            return errorMsg{err}
        }
        return backendStatusMsg{
            available: true,
            version:   status.Version,
        }
    }
}

// ✅ CORRECTO: commands con parámetros
func generateCode(plan AgentPlan) tea.Cmd {
    return func() tea.Msg {
        code, err := client.GenerateCode(context.Background(), plan)
        if err != nil {
            return errorMsg{err}
        }
        return codeGeneratedMsg{
            code:     code,
            filename: formatFilename(plan.Nombre),
        }
    }
}
```

---

## 🎨 Lipgloss Patterns

### Definición de Estilos

```go
// ✅ CORRECTO: estilos como variables del paquete
package styles

var (
    // Base styles
    BaseStyle = lipgloss.NewStyle().
        Padding(1, 2).
        Margin(1, 0)
    
    // Semantic styles
    SuccessStyle = BaseStyle.
        Foreground(lipgloss.Color("#A3BE8C")).
        Bold(true)
    
    ErrorStyle = BaseStyle.
        Foreground(lipgloss.Color("#BF616A")).
        Bold(true)
    
    // Component styles
    BoxStyle = lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("#434C5E")).
        Padding(1, 2)
)

// ✅ CORRECTO: funciones para estilos dinámicos
func ProgressBarStyle(percentage int) lipgloss.Style {
    color := lipgloss.Color("#EBCB8B") // warning
    if percentage >= 100 {
        color = lipgloss.Color("#A3BE8C") // success
    }
    
    return lipgloss.NewStyle().
        Foreground(color).
        Bold(true)
}
```

### Composición de Layouts

```go
// ✅ CORRECTO: usar Join* para layouts
func renderTwoColumns(left, right string) string {
    leftBox := BoxStyle.Width(40).Render(left)
    rightBox := BoxStyle.Width(40).Render(right)
    
    return lipgloss.JoinHorizontal(
        lipgloss.Top,
        leftBox,
        rightBox,
    )
}

func renderHeader(title string) string {
    logo := "🤖"
    titleText := lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("#88C0D0")).
        Render(title)
    
    return lipgloss.JoinHorizontal(
        lipgloss.Center,
        logo,
        " ",
        titleText,
    )
}

// ✅ CORRECTO: calcular tamaños dinámicamente
func renderFullWidth(content string, width int) string {
    return lipgloss.NewStyle().
        Width(width).
        Align(lipgloss.Center).
        Render(content)
}
```

---

## 🔧 Error Handling

### Patrones Básicos

```go
// ✅ CORRECTO: siempre verificar errores
result, err := client.CreatePlan(ctx, request)
if err != nil {
    return nil, fmt.Errorf("failed to create plan: %w", err)
}

// ✅ CORRECTO: usar %w para wrapping
if err := validatePlan(plan); err != nil {
    return fmt.Errorf("plan validation failed: %w", err)
}

// ✅ CORRECTO: errores custom con contexto
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %s: %s", e.Field, e.Message)
}

// ✅ CORRECTO: defer para cleanup
func readConfig(path string) (*Config, error) {
    file, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer file.Close()
    
    // ... leer archivo
}

// ❌ INCORRECTO: ignorar errores
result, _ := client.CreatePlan(ctx, request) // MAL!

// ❌ INCORRECTO: panic en código de aplicación
if err != nil {
    panic(err) // Solo en init() o casos críticos
}
```

### Error Messages

```go
// ✅ CORRECTO: mensajes descriptivos y accionables
return fmt.Errorf("failed to connect to backend at %s: %w (is the server running?)", url, err)

// ✅ CORRECTO: incluir valores relevantes
return fmt.Errorf("invalid plan level %d (must be between 1 and 5)", level)

// ❌ INCORRECTO: mensajes vagos
return errors.New("error") // ¿Qué error?
return fmt.Errorf("failed") // ¿Qué falló?
```

---

## 🧪 Testing

### Nomenclatura de Tests

```go
// ✅ CORRECTO: Test + Nombre de función/caso
func TestCreatePlan(t *testing.T) {}
func TestCreatePlan_InvalidInput(t *testing.T) {}
func TestCreatePlan_NetworkError(t *testing.T) {}

// ✅ CORRECTO: subtests con t.Run
func TestAgentPlan(t *testing.T) {
    t.Run("valid plan", func(t *testing.T) {
        // ...
    })
    
    t.Run("missing required fields", func(t *testing.T) {
        // ...
    })
}
```

### Estructura de Tests

```go
// ✅ CORRECTO: patrón Arrange-Act-Assert
func TestGenerateCode(t *testing.T) {
    // Arrange
    plan := models.AgentPlan{
        Nombre: "Test Agent",
        Rol:    "Testing",
        Nivel:  1,
    }
    generator := NewCodeGenerator()
    
    // Act
    code, err := generator.Generate(plan)
    
    // Assert
    require.NoError(t, err)
    assert.Contains(t, code, "Test Agent")
    assert.Contains(t, code, "from agno.agent import Agent")
}

// ✅ CORRECTO: table-driven tests
func TestValidateLevel(t *testing.T) {
    tests := []struct {
        name    string
        level   int
        wantErr bool
    }{
        {"valid level 1", 1, false},
        {"valid level 5", 5, false},
        {"invalid level 0", 0, true},
        {"invalid level 6", 6, true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateLevel(tt.level)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

### Mocking

```go
// ✅ CORRECTO: interfaces para mocking
type MetaAgentClient interface {
    CreatePlan(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error)
}

// Mock implementation
type mockClient struct {
    createPlanFunc func(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error)
}

func (m *mockClient) CreatePlan(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error) {
    if m.createPlanFunc != nil {
        return m.createPlanFunc(ctx, req)
    }
    return &PlanResponse{}, nil
}

// Uso en test
func TestWithMock(t *testing.T) {
    mock := &mockClient{
        createPlanFunc: func(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error) {
            return &PlanResponse{
                Plan: models.AgentPlan{Nombre: "Mocked"},
            }, nil
        },
    }
    
    // Test con mock
    result, err := mock.CreatePlan(context.Background(), CreatePlanRequest{})
    assert.NoError(t, err)
    assert.Equal(t, "Mocked", result.Plan.Nombre)
}
```

---

## 📦 Gestión de Dependencias

### Context

```go
// ✅ CORRECTO: siempre pasar context como primer parámetro
func CreatePlan(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error)

// ✅ CORRECTO: propagar context
func (c *Client) CreatePlan(ctx context.Context, req CreatePlanRequest) (*PlanResponse, error) {
    return c.httpClient.Post(ctx, "/api/v1/plan/create", req)
}

// ✅ CORRECTO: usar context para timeouts
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

result, err := client.CreatePlan(ctx, request)

// ❌ INCORRECTO: context.Background() en funciones
func CreatePlan(req CreatePlanRequest) (*PlanResponse, error) {
    ctx := context.Background() // debería recibir context
    // ...
}
```

### Dependency Injection

```go
// ✅ CORRECTO: inyección por constructor
type ConversationScreen struct {
    client client.MetaAgentClient
    config *config.Config
}

func NewConversationScreen(client client.MetaAgentClient, cfg *config.Config) *ConversationScreen {
    return &ConversationScreen{
        client: client,
        config: cfg,
    }
}

// ✅ CORRECTO: interfaces para flexibilidad
type Logger interface {
    Info(msg string)
    Error(msg string, err error)
}

// Permite inyectar diferentes implementaciones
func NewApp(logger Logger) *App {
    return &App{logger: logger}
}
```

---

## 🚀 Performance

### Strings y Formatting

```go
// ✅ CORRECTO: usar strings.Builder para concatenación
var sb strings.Builder
for _, line := range lines {
    sb.WriteString(line)
    sb.WriteString("\n")
}
result := sb.String()

// ❌ INCORRECTO: concatenación repetida
var result string
for _, line := range lines {
    result += line + "\n" // Muy lento para muchas líneas
}

// ✅ CORRECTO: fmt.Sprintf para formateo simple
msg := fmt.Sprintf("User %s logged in at %s", user, time.Now())

// ❌ INCORRECTO: concatenación manual
msg := "User " + user + " logged in at " + time.Now().String()
```

### Slices y Maps

```go
// ✅ CORRECTO: pre-allocar con capacidad conocida
messages := make([]Message, 0, expectedCount)

// ✅ CORRECTO: usar make para maps
cache := make(map[string]*AgentPlan, 100)

// ❌ INCORRECTO: append en loop sin capacidad
var messages []Message
for i := 0; i < 1000; i++ {
    messages = append(messages, Message{}) // Múltiples reallocaciones
}
```

### Goroutines

```go
// ✅ CORRECTO: usar goroutines para operaciones async
func fetchData() tea.Cmd {
    return func() tea.Msg {
        // Esta función corre en goroutine
        data, err := client.FetchData()
        if err != nil {
            return errorMsg{err}
        }
        return dataFetchedMsg{data}
    }
}

// ✅ CORRECTO: usar sync.WaitGroup para coordinación
var wg sync.WaitGroup
for _, url := range urls {
    wg.Add(1)
    go func(u string) {
        defer wg.Done()
        fetch(u)
    }(url)
}
wg.Wait()

// ❌ INCORRECTO: goroutine leak
go func() {
    for {
        // Sin manera de detener esta goroutine
        doWork()
    }
}()
```

---

## 📚 Documentación

### Comments

```go
// ✅ CORRECTO: comentario de package
// Package screens contiene las pantallas principales de la UI.
// Cada pantalla implementa el patrón Model-View-Update de Bubble Tea.
package screens

// ✅ CORRECTO: comentario de función exportada
// NewConversationScreen crea una nueva pantalla de conversación
// con el cliente especificado y configuración por defecto.
func NewConversationScreen(client client.MetaAgentClient) *ConversationScreen {
    // ...
}

// ✅ CORRECTO: comentario de type exportado
// AgentPlan representa la especificación completa de un agente AI.
// Contiene toda la información necesaria para generar el código del agente.
type AgentPlan struct {
    // Nombre es el identificador único del agente
    Nombre string
    
    // Nivel define la complejidad (1-5)
    Nivel int
}

// ✅ CORRECTO: explicar "por qué", no "qué"
// Usamos un buffer de 1024 porque el promedio de respuestas
// del servidor es ~800 bytes, y queremos evitar reallocaciones.
const bufferSize = 1024

// ❌ INCORRECTO: comentario obvio
// Esta función suma dos números
func Add(a, b int) int { return a + b }
```

### Ejemplos

```go
// ✅ CORRECTO: añadir ejemplos para funcionalidad compleja
// Example:
//
//   style := NewProgressBarStyle(75)
//   bar := style.Render("████████░░")
//
func NewProgressBarStyle(percentage int) lipgloss.Style {
    // ...
}
```

---

## ✅ Checklist de Code Review

Antes de hacer PR, verificar:

**General:**
- [ ] Código sigue convenciones de nomenclatura
- [ ] Sin imports no utilizados
- [ ] Sin variables no utilizadas
- [ ] `gofmt` aplicado
- [ ] `golangci-lint` pasa sin errores

**Error Handling:**
- [ ] Todos los errores verificados
- [ ] Errores wrapeados con contexto
- [ ] No hay `panic()` en código de aplicación

**Testing:**
- [ ] Tests añadidos para nueva funcionalidad
- [ ] Tests pasan (`go test ./...`)
- [ ] Cobertura razonable (>70%)

**Documentation:**
- [ ] Funciones exportadas tienen comentarios
- [ ] Comentarios explican "por qué", no "qué"
- [ ] README actualizado si es necesario

**Performance:**
- [ ] No hay allocaciones innecesarias en hot paths
- [ ] Strings.Builder usado para concatenación en loops
- [ ] Context propagado correctamente

**Bubble Tea Specific:**
- [ ] Models no modifican estado global
- [ ] Commands retornan tea.Cmd
- [ ] View() es puro (sin side effects)
- [ ] Messages bien tipadas

---

## 🔗 Referencias

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
- [Bubble Tea Best Practices](https://github.com/charmbracelet/bubbletea/tree/master/tutorials)

---

**Última actualización:** Octubre 14, 2025  
**Mantenedor:** Frontend Team  
**Estado:** 📘 Living Document (actualizar según evolucionemos)

