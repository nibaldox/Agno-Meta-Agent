# Lantui - Meta-Agent TUI

Terminal UI moderna para el Meta-Agente Generador de Agentes AI.

## 🚀 Quick Start

### Requisitos

- Go 1.21 o superior
- AgentOS corriendo en `http://localhost:7777`

### Instalación

```bash
# Instalar dependencias
cd lantui
go mod download

# Ejecutar
go run cmd/lantui/main.go
```

### Desarrollo

```bash
# Build
go build -o bin/lantui cmd/lantui/main.go

# Run
./bin/lantui

# Tests
go test ./...
```

## 📚 Documentación

Ver documentación completa en `../doc-frontend/`

- [Setup Inicial](../doc-frontend/setup-inicial.md)
- [API Contracts](../doc-frontend/api-contracts-agentos.md)
- [Guía de Estilo Go](../doc-frontend/guia-estilo-go.md)

## 🏗️ Arquitectura

```
lantui/
├── cmd/lantui/          # Entry point
├── internal/
│   ├── app/             # Aplicación principal
│   ├── ui/              # Componentes UI
│   │   ├── screens/     # Pantallas
│   │   ├── components/  # Widgets
│   │   └── styles/      # Temas
│   ├── client/          # Cliente AgentOS
│   └── models/          # Estructuras de datos
└── pkg/utils/           # Utilidades compartidas
```

## 🎨 Stack

- **Bubble Tea** - Framework TUI
- **Lipgloss** - Styling
- **Bubbles** - Componentes pre-construidos

## 📝 Estado

- [x] Estructura inicial
- [ ] Pantalla Welcome
- [ ] Cliente AgentOS
- [ ] Screens completas
- [ ] Integración con backend

## 🤝 Contribuir

Ver guías en `doc-frontend/`

