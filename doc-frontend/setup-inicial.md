# Setup Inicial - Lantui Development

> **Guía completa para configurar el entorno de desarrollo del frontend TUI**  
> **Stack:** Go 1.21+, Bubble Tea, Lipgloss, Charm Suite

---

## 📋 Pre-requisitos

### Software Requerido

1. **Go 1.21 o superior**
   ```bash
   # Verificar versión
   go version
   
   # Descargar: https://go.dev/dl/
   ```

2. **Git**
   ```bash
   git --version
   ```

3. **Make** (opcional pero recomendado)
   ```bash
   # Windows: choco install make
   # macOS: xcode-select --install
   # Linux: sudo apt install build-essential
   ```

4. **Terminal con soporte de colores**
   - Windows: Windows Terminal (recomendado)
   - macOS: iTerm2 o Terminal.app
   - Linux: Gnome Terminal, Konsole, etc.

### Conocimientos Recomendados

- Go básico (syntax, structs, interfaces)
- Conceptos de TUI (terminal user interface)
- Arquitectura Elm (Model-View-Update) - útil para Bubble Tea

---

## 🚀 Setup Paso a Paso

### 1. Clonar Repositorio

```bash
# Si no lo has clonado aún
git clone https://github.com/tuorg/meta-agent.git
cd meta-agent
```

### 2. Crear Estructura Lantui

```bash
# Crear carpeta principal
mkdir lantui
cd lantui

# Inicializar módulo Go
go mod init github.com/tuorg/meta-agent/lantui

# Crear estructura de carpetas
mkdir -p cmd/lantui
mkdir -p internal/{app,ui/{components,screens,styles},client,models,config}
mkdir -p pkg/utils
mkdir -p assets
mkdir -p testdata/{requests,responses}
```

**Resultado:**
```
lantui/
├── cmd/
│   └── lantui/
│       └── main.go
├── internal/
│   ├── app/
│   ├── ui/
│   │   ├── components/
│   │   ├── screens/
│   │   └── styles/
│   ├── client/
│   ├── models/
│   └── config/
├── pkg/
│   └── utils/
├── assets/
├── testdata/
├── go.mod
└── go.sum
```

### 3. Instalar Dependencias

```bash
# Core framework
go get github.com/charmbracelet/bubbletea@latest
go get github.com/charmbracelet/lipgloss@latest
go get github.com/charmbracelet/bubbles@latest

# Markdown rendering
go get github.com/charmbracelet/glamour@latest

# Configuración
go get github.com/spf13/viper@latest

# HTTP client
go get github.com/go-resty/resty/v2@latest

# Testing
go get github.com/stretchr/testify@latest

# Logging (opcional)
go get github.com/charmbracelet/log@latest
```

**Resultado `go.mod`:**
```go
module github.com/tuorg/meta-agent/lantui

go 1.21

require (
    github.com/charmbracelet/bubbles v0.18.0
    github.com/charmbracelet/bubbletea v0.27.0
    github.com/charmbracelet/glamour v0.7.0
    github.com/charmbracelet/lipgloss v0.13.0
    github.com/go-resty/resty/v2 v2.11.0
    github.com/spf13/viper v1.18.2
    github.com/stretchr/testify v1.9.0
)
```

### 4. Crear Archivo Main Inicial

```bash
# Crear main.go
cat > cmd/lantui/main.go << 'EOF'
package main

import (
    "fmt"
    "os"

    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

// Model es el estado de la aplicación
type model struct {
    ready bool
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
        case "q", "ctrl+c":
            return m, tea.Quit
        case "enter":
            m.ready = true
        }
    }
    return m, nil
}

// View renderiza la UI
func (m model) View() string {
    if !m.ready {
        return welcomeView()
    }
    return runningView()
}

func welcomeView() string {
    style := lipgloss.NewStyle().
        Foreground(lipgloss.Color("#88C0D0")).
        Bold(true).
        Padding(1, 2).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("#434C5E"))

    content := lipgloss.JoinVertical(
        lipgloss.Center,
        "🤖  Meta-Agente Generador",
        "",
        "Crea agentes AI personalizados",
        "",
        "[Presiona ENTER para comenzar]",
        "[Presiona Q para salir]",
    )

    return style.Render(content)
}

func runningView() string {
    return "✓ Aplicación funcionando!\n\nPresiona Q para salir."
}

func main() {
    // Crear modelo inicial
    m := model{ready: false}

    // Iniciar programa Bubble Tea
    p := tea.NewProgram(m, tea.WithAltScreen())

    // Ejecutar
    if _, err := p.Run(); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
}
EOF
```

### 5. Probar Instalación

```bash
# Compilar
go build -o bin/lantui cmd/lantui/main.go

# Ejecutar
./bin/lantui

# O directamente
go run cmd/lantui/main.go
```

**Deberías ver:**
```
╭──────────────────────────────────╮
│                                  │
│  🤖  Meta-Agente Generador      │
│                                  │
│  Crea agentes AI personalizados  │
│                                  │
│  [Presiona ENTER para comenzar]  │
│  [Presiona Q para salir]         │
│                                  │
╰──────────────────────────────────╯
```

---

## 🛠️ Herramientas de Desarrollo

### Air (Live Reload)

Instalar:
```bash
go install github.com/cosmtrek/air@latest
```

Configurar (`.air.toml`):
```toml
root = "."
testdata_dir = "testdata"
tmp_dir = "tmp"

[build]
  args_bin = []
  bin = "./tmp/lantui"
  cmd = "go build -o ./tmp/lantui cmd/lantui/main.go"
  delay = 1000
  exclude_dir = ["assets", "tmp", "vendor", "testdata"]
  exclude_file = []
  exclude_regex = ["_test.go"]
  exclude_unchanged = false
  follow_symlink = false
  full_bin = ""
  include_dir = []
  include_ext = ["go", "tpl", "tmpl", "html"]
  include_file = []
  kill_delay = "0s"
  log = "build-errors.log"
  poll = false
  poll_interval = 0
  rerun = false
  rerun_delay = 500
  send_interrupt = false
  stop_on_error = false

[color]
  app = ""
  build = "yellow"
  main = "magenta"
  runner = "green"
  watcher = "cyan"

[log]
  main_only = false
  time = false

[misc]
  clean_on_exit = false

[screen]
  clear_on_rebuild = false
  keep_scroll = true
```

Usar:
```bash
# Desarrollo con live reload
air
```

### golangci-lint

Instalar:
```bash
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

Configurar (`.golangci.yml`):
```yaml
linters:
  enable:
    - gofmt
    - govet
    - errcheck
    - staticcheck
    - unused
    - gosimple
    - structcheck
    - varcheck
    - ineffassign
    - deadcode
    - typecheck

linters-settings:
  gofmt:
    simplify: true

run:
  timeout: 5m
  tests: true
  skip-dirs:
    - tmp
    - vendor
```

Usar:
```bash
# Linting
golangci-lint run

# Fix automático
golangci-lint run --fix
```

### Task (Build Tool)

Instalar:
```bash
go install github.com/go-task/task/v3/cmd/task@latest
```

Configurar (`Taskfile.yml`):
```yaml
version: '3'

tasks:
  default:
    desc: "Mostrar ayuda"
    cmds:
      - task --list

  build:
    desc: "Compilar aplicación"
    cmds:
      - go build -o bin/lantui cmd/lantui/main.go

  run:
    desc: "Ejecutar aplicación"
    cmds:
      - go run cmd/lantui/main.go

  dev:
    desc: "Desarrollo con live reload"
    cmds:
      - air

  test:
    desc: "Ejecutar tests"
    cmds:
      - go test -v ./...

  test-coverage:
    desc: "Tests con cobertura"
    cmds:
      - go test -v -coverprofile=coverage.out ./...
      - go tool cover -html=coverage.out -o coverage.html

  lint:
    desc: "Linting"
    cmds:
      - golangci-lint run

  lint-fix:
    desc: "Linting con fix automático"
    cmds:
      - golangci-lint run --fix

  clean:
    desc: "Limpiar archivos generados"
    cmds:
      - rm -rf bin tmp coverage.out coverage.html

  deps:
    desc: "Actualizar dependencias"
    cmds:
      - go get -u ./...
      - go mod tidy

  install:
    desc: "Instalar herramientas de desarrollo"
    cmds:
      - go install github.com/cosmtrek/air@latest
      - go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

Usar:
```bash
# Ver comandos disponibles
task

# Compilar
task build

# Ejecutar
task run

# Desarrollo
task dev

# Tests
task test

# Linting
task lint
```

---

## 🧪 Testing Setup

### Estructura de Tests

```bash
# Crear estructura de tests
mkdir -p internal/ui/components/components_test
mkdir -p internal/client/client_test
```

### Ejemplo de Test

```go
// internal/ui/styles/theme_test.go
package styles

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestThemeColors(t *testing.T) {
    theme := DefaultTheme

    assert.NotEmpty(t, theme.Primary)
    assert.NotEmpty(t, theme.Secondary)
    assert.NotEmpty(t, theme.Success)
}
```

### Ejecutar Tests

```bash
# Todos los tests
go test ./...

# Con verbose
go test -v ./...

# Con cobertura
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Test específico
go test -v ./internal/ui/styles -run TestThemeColors
```

---

## 🎨 Editor Setup

### VS Code

**Extensiones recomendadas:**
```json
{
  "recommendations": [
    "golang.go",
    "ms-vscode.makefile-tools",
    "tamasfe.even-better-toml",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

**Configuración (`.vscode/settings.json`):**
```json
{
  "go.useLanguageServer": true,
  "go.lintTool": "golangci-lint",
  "go.lintOnSave": "workspace",
  "go.formatTool": "gofmt",
  "[go]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "go.testFlags": ["-v"],
  "go.coverOnSave": true
}
```

### GoLand / IntelliJ IDEA

1. Abrir proyecto `lantui/`
2. Go to `Settings > Go > Go Modules`
3. Enable `Enable Go modules integration`
4. Go to `Settings > Tools > File Watchers`
5. Add `gofmt` y `golangci-lint`

---

## 📁 Archivos Adicionales

### Makefile

```makefile
.PHONY: all build run dev test lint clean help

# Variables
BINARY_NAME=lantui
BUILD_DIR=bin
MAIN_PATH=cmd/lantui/main.go

all: help

build: ## Compilar aplicación
	@echo "Building..."
	@go build -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)

run: ## Ejecutar aplicación
	@go run $(MAIN_PATH)

dev: ## Desarrollo con live reload
	@air

test: ## Ejecutar tests
	@go test -v ./...

test-coverage: ## Tests con cobertura
	@go test -v -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html

lint: ## Linting
	@golangci-lint run

lint-fix: ## Linting con fix
	@golangci-lint run --fix

clean: ## Limpiar archivos generados
	@rm -rf $(BUILD_DIR) tmp coverage.out coverage.html

deps: ## Actualizar dependencias
	@go get -u ./...
	@go mod tidy

install-tools: ## Instalar herramientas dev
	@go install github.com/cosmtrek/air@latest
	@go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
```

### .gitignore

```gitignore
# Binaries
bin/
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary
*.test

# Output of the go coverage tool
*.out
coverage.html

# Dependency directories
vendor/

# Go workspace file
go.work

# Air
tmp/
.air.toml.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

---

## ✅ Verificación Final

Ejecuta estos comandos para verificar que todo está configurado:

```bash
# 1. Versión de Go
go version

# 2. Dependencias instaladas
go list -m all

# 3. Build exitoso
go build -o bin/lantui cmd/lantui/main.go

# 4. Tests pasan
go test ./...

# 5. Linting pasa
golangci-lint run

# 6. Ejecutar aplicación
./bin/lantui
```

**Checklist:**
- [ ] Go 1.21+ instalado
- [ ] Dependencias descargadas
- [ ] Build exitoso
- [ ] Tests pasan
- [ ] Linting sin errores
- [ ] Aplicación se ejecuta y muestra pantalla de bienvenida

---

## 🆘 Troubleshooting

### "command not found: go"

**Solución:**
- Windows: Agregar Go a PATH
- macOS/Linux: Agregar `export PATH=$PATH:/usr/local/go/bin` a `.bashrc` o `.zshrc`

### "module not found"

**Solución:**
```bash
go mod download
go mod tidy
```

### "air: command not found"

**Solución:**
```bash
# Verificar GOPATH/bin en PATH
echo $GOPATH/bin  # Unix
echo %GOPATH%\bin # Windows

# Reinstalar
go install github.com/cosmtrek/air@latest
```

### Terminal no muestra colores

**Solución:**
- Windows: Usar Windows Terminal
- Verificar variable: `echo $TERM` debe ser `xterm-256color` o similar

---

## 🎓 Recursos de Aprendizaje

### Bubble Tea
- [Tutorial oficial](https://github.com/charmbracelet/bubbletea/tree/master/tutorials)
- [Ejemplos](https://github.com/charmbracelet/bubbletea/tree/master/examples)
- [Documentation](https://pkg.go.dev/github.com/charmbracelet/bubbletea)

### Lipgloss
- [README](https://github.com/charmbracelet/lipgloss)
- [Ejemplos](https://github.com/charmbracelet/lipgloss/tree/master/examples)

### Go Patterns
- [Effective Go](https://go.dev/doc/effective_go)
- [Go by Example](https://gobyexample.com/)

---

## 📞 Soporte

**Problemas con setup:**
- Crear issue en GitHub
- Etiquetar como `setup` o `help-wanted`
- Incluir output de `go version` y `go env`

**Preguntas:**
- Documentación: `doc-frontend/`
- Team lead: [Nombre]
- Canal: #lantui-dev

---

**¡Listo para comenzar el desarrollo!** 🚀

Siguiente paso: [Plan de Desarrollo](./plan-desarrollo-lantui.md)

