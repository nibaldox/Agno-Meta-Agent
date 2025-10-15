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

test: ## Ejecutar tests
	@go test -v ./...

test-coverage: ## Tests con cobertura
	@go test -v -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report: coverage.html"

lint: ## Linting (requiere golangci-lint)
	@golangci-lint run || echo "golangci-lint no instalado. Instala con: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest"

fmt: ## Formatear código
	@go fmt ./...
	@echo "Código formateado"

deps: ## Descargar dependencias
	@go mod download
	@go mod tidy
	@echo "Dependencias actualizadas"

clean: ## Limpiar archivos generados
	@rm -rf $(BUILD_DIR) coverage.out coverage.html
	@echo "Limpieza completada"

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

