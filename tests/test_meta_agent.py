"""Tests unitarios para `MetaAgent`."""

import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.application.services.meta_agent import AgentPlan, MetaAgent


def _ensure_stub_agno_modules() -> None:
    """Registra módulos stub de `agno` para las pruebas unitarias."""

    if "agno.agent" not in sys.modules:
        agent_module = ModuleType("agno.agent")

        class StubAgent:  # pragma: no cover - stub
            def __init__(self, **kwargs):
                self.kwargs = kwargs
                self.run = MagicMock()

        agent_module.Agent = StubAgent
        sys.modules["agno.agent"] = agent_module

    if "agno.models" not in sys.modules:
        sys.modules["agno.models"] = ModuleType("agno.models")

    if "agno.models.deepseek" not in sys.modules:
        deepseek_module = ModuleType("agno.models.deepseek")

        class StubDeepSeek:  # pragma: no cover - stub
            def __init__(self, id: str):
                self.id = id

        deepseek_module.DeepSeek = StubDeepSeek
        sys.modules["agno.models.deepseek"] = deepseek_module


_ensure_stub_agno_modules()


def _build_plan_dict(**overrides) -> dict:
    base = {
        "nombre": "Agente Demo",
        "rol": "Asistente de prueba",
        "modelo": "deepseek-chat",
        "nivel": 1,
        "herramientas": [],
        "instrucciones": ["Sé útil"],
        "necesita_memoria": False,
        "es_equipo": False,
        "miembros_equipo": [],
        "ejemplo_uso": "¿Cuál es el estado?",
    }
    base.update(overrides)
    return base


class TestCreatePlan:
    def test_create_plan_with_clean_json(self, meta_agent: MetaAgent) -> None:
        plan_dict = _build_plan_dict(nombre="Plan JSON Limpio")
        meta_agent.planner_agent.run.return_value = SimpleNamespace(
            content=json.dumps(plan_dict)
        )

        plan = meta_agent.create_plan("Conversación simulada")

        assert isinstance(plan, AgentPlan)
        assert plan.nombre == "Plan JSON Limpio"

    def test_create_plan_with_markdown_wrapped_json(
        self, meta_agent: MetaAgent
    ) -> None:
        plan_dict = _build_plan_dict(nombre="Plan Markdown")
        markdown_content = f"```json\n{json.dumps(plan_dict)}\n```"
        meta_agent.planner_agent.run.return_value = SimpleNamespace(
            content=markdown_content
        )

        plan = meta_agent.create_plan("Conversación simulada")

        assert plan.nombre == "Plan Markdown"

    def test_create_plan_invalid_json_raises(self, meta_agent: MetaAgent) -> None:
        meta_agent.planner_agent.run.return_value = SimpleNamespace(
            content="Respuesta no válida"
        )

        with pytest.raises(ValueError):
            meta_agent.create_plan("Conversación simulada")


class TestGenerateCode:
    def test_generate_code_basic_agent(
        self, meta_agent: MetaAgent, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_basic = MagicMock(return_value="basic-code")
        mock_memory = MagicMock()
        mock_team = MagicMock()

        monkeypatch.setattr(
            "src.infrastructure.templates.agent_templates.AgentTemplate.generate_basic_agent",
            mock_basic,
        )
        monkeypatch.setattr(
            "src.infrastructure.templates.agent_templates.AgentTemplate.generate_agent_with_memory",
            mock_memory,
        )
        monkeypatch.setattr(
            "src.infrastructure.templates.agent_templates.AgentTemplate.generate_agent_team",
            mock_team,
        )

        plan = AgentPlan(**_build_plan_dict(modelo="gpt-4o"))

        result = meta_agent.generate_code(plan)

        assert result == "basic-code"
        mock_basic.assert_called_once()
        mock_memory.assert_not_called()
        mock_team.assert_not_called()

    def test_generate_code_memory_agent(
        self, meta_agent: MetaAgent, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_memory = MagicMock(return_value="memory-code")
        mock_basic = MagicMock()

        monkeypatch.setattr(
            "src.infrastructure.templates.agent_templates.AgentTemplate.generate_agent_with_memory",
            mock_memory,
        )
        monkeypatch.setattr(
            "src.infrastructure.templates.agent_templates.AgentTemplate.generate_basic_agent",
            mock_basic,
        )

        plan = AgentPlan(**_build_plan_dict(nivel=3, necesita_memoria=False))

        result = meta_agent.generate_code(plan)

        assert result == "memory-code"
        mock_memory.assert_called_once()
        mock_basic.assert_not_called()

    def test_generate_code_team_agent_adjusts_model(
        self, meta_agent: MetaAgent, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_team = MagicMock(return_value="team-code")
        monkeypatch.setattr(
            "src.infrastructure.templates.agent_templates.AgentTemplate.generate_agent_team",
            mock_team,
        )

        plan = AgentPlan(**_build_plan_dict(es_equipo=True, modelo="deepseek-chat"))

        result = meta_agent.generate_code(plan)

        assert result == "team-code"
        mock_team.assert_called_once()
        assert plan.modelo == "deepseek-reasoner"


class TestInteractiveCreation:
    def test_interactive_creation_generates_agent_file(
        self,
        meta_agent: MetaAgent,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        # Forzar que el analyzer determine información completa desde el inicio
        meta_agent.analyzer_agent.run.return_value = SimpleNamespace(
            content="INFO_COMPLETA"
        )

        plan = AgentPlan(**_build_plan_dict(nombre="Agente Interactivo"))
        captured_conversation: dict[str, str] = {}

        def fake_create_plan(conversation: str) -> AgentPlan:
            captured_conversation["value"] = conversation
            return plan

        generate_code_mock = MagicMock(return_value="print('listo')\n")

        monkeypatch.setattr(meta_agent, "create_plan", fake_create_plan)
        monkeypatch.setattr(meta_agent, "generate_code", generate_code_mock)

        inputs = iter(["Necesito un agente interactivo", "s"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

        from src.application.services import meta_agent as meta_agent_module

        stub_console = SimpleNamespace(print=lambda *args, **kwargs: None)
        monkeypatch.setattr(meta_agent_module, "console", stub_console)
        monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))

        meta_agent.interactive_creation()

        expected_file = (
            tmp_path / "generated" / "agents" / "agente_interactivo_agent.py"
        )
        assert expected_file.exists()
        assert expected_file.read_text(encoding="utf-8") == "print('listo')\n"

        assert "Necesito un agente interactivo" in captured_conversation.get(
            "value", ""
        )
        generate_code_mock.assert_called_once_with(plan)

    def test_interactive_creation_cancelled_by_user(
        self,
        meta_agent: MetaAgent,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        meta_agent.analyzer_agent.run.return_value = SimpleNamespace(
            content="INFO_COMPLETA"
        )

        def fake_create_plan(_: str) -> AgentPlan:
            return AgentPlan(**_build_plan_dict(nombre="Agente Cancelado"))

        monkeypatch.setattr(meta_agent, "create_plan", fake_create_plan)
        generate_code_mock = MagicMock()
        monkeypatch.setattr(meta_agent, "generate_code", generate_code_mock)

        inputs = iter(["Quiero un agente cancelado", "n"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        from src.application.services import meta_agent as meta_agent_module

        monkeypatch.setattr(
            meta_agent_module,
            "console",
            SimpleNamespace(print=lambda *args, **kwargs: None),
        )
        monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))

        meta_agent.interactive_creation()

        expected_file = tmp_path / "generated" / "agents" / "agente_cancelado_agent.py"
        assert not expected_file.exists()
        generate_code_mock.assert_not_called()

    def test_interactive_creation_plan_error(
        self,
        meta_agent: MetaAgent,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        meta_agent.analyzer_agent.run.return_value = SimpleNamespace(
            content="INFO_COMPLETA"
        )

        def fake_create_plan(_: str) -> AgentPlan:
            raise ValueError("Error planeando")

        monkeypatch.setattr(meta_agent, "create_plan", fake_create_plan)
        generate_code_mock = MagicMock()
        monkeypatch.setattr(meta_agent, "generate_code", generate_code_mock)

        inputs = iter(
            ["Genera un agente que falla"]
        )  # se cancelará al lanzar excepción
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        from src.application.services import meta_agent as meta_agent_module

        monkeypatch.setattr(
            meta_agent_module,
            "console",
            SimpleNamespace(print=lambda *args, **kwargs: None),
        )
        monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))

        meta_agent.interactive_creation()

        # No debe generarse archivo ni llamarse a generate_code
        assert not any((tmp_path / "generated").rglob("*.py"))
        generate_code_mock.assert_not_called()


@pytest.fixture
def meta_agent(monkeypatch: pytest.MonkeyPatch) -> MetaAgent:
    """Devuelve una instancia de MetaAgent con dependencias mockeadas."""

    class FakeAgent:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.run = MagicMock()

    class FakeDeepSeek:
        def __init__(self, id: str):
            self.id = id

    monkeypatch.setattr("src.application.services.meta_agent.Agent", FakeAgent)
    monkeypatch.setattr("src.application.services.meta_agent.DeepSeek", FakeDeepSeek)
    return MetaAgent()
