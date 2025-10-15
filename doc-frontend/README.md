# Documentación Frontend - Lantui

Bienvenido a la documentación del frontend TUI para el Meta-Agente Generador.

## 📁 Estructura de Documentación

### 📖 Inicio Rápido

- **[resumen-agentos.md](./resumen-agentos.md)** - ⭐ **EMPIEZA AQUÍ** - Resumen ejecutivo de Lantui + AgentOS

### Documentos Principales

- **[plan-desarrollo-lantui.md](./plan-desarrollo-lantui.md)** - Plan completo de desarrollo, arquitectura y cronograma
- **[api-contracts-agentos.md](./api-contracts-agentos.md)** - ✅ Contratos de API con AgentOS
- **[setup-inicial.md](./setup-inicial.md)** - ✅ Guía completa de setup del entorno Go
- **[guia-estilo-go.md](./guia-estilo-go.md)** - ✅ Guía de estilos y mejores prácticas

### Documentos Legacy
- **api-contracts.md** - (Obsoleto) Reemplazado por api-contracts-agentos.md

## 🎯 Estado Actual

**Fase:** Planificación y Documentación  
**Progreso:** 15%  
**Última actualización:** Octubre 14, 2025

### Decisiones Arquitectónicas

✅ **Backend: AgentOS** (Agno Framework)
- API RESTful completa incluida
- Gestión de sesiones automática
- Storage SQLite para persistencia
- Multi-agente nativo

✅ **Frontend: Bubble Tea** (Go)
- UI moderna estilo Claude Code
- Componentes reutilizables con Lipgloss
- Streaming y animaciones
- Desarrollo paralelo con mocks

### Próximos Pasos

1. ✅ Plan de desarrollo documentado
2. ✅ Contratos de API con AgentOS definidos
3. ✅ Guías de setup y estilo
4. ⏳ Crear archivo `agentos.py` en backend
5. ⏳ Setup inicial del proyecto Go (carpeta lantui/)
6. ⏳ Implementación de pantalla Welcome
7. ⏳ Cliente Go para AgentOS API

## 🔗 Enlaces Rápidos

### Recursos Externos
- [Bubble Tea Tutorial](https://github.com/charmbracelet/bubbletea/tree/master/tutorials)
- [Lipgloss Examples](https://github.com/charmbracelet/lipgloss/tree/master/examples)
- [Charm Style Guide](https://charm.sh/style)

### Repositorio Principal
- [Meta-Agente Backend (Python)](../src/)
- [Agentes Generados](../generated/agents/)
- [Tests](../tests/)

## 📝 Convenciones

- Todos los documentos en formato Markdown
- Usar español para documentación de usuario
- Código y comentarios en inglés (estándar Go)
- Diagramas con Mermaid cuando sea posible

## 👥 Equipo

**Frontend Lead:** [Por asignar]  
**Backend Team:** Python + Agno Framework  
**Colaboración:** Desarrollo paralelo con contratos mínimos

---

Para comenzar, lee primero el [Plan de Desarrollo](./plan-desarrollo-lantui.md).

