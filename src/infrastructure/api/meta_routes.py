"""
Rutas custom de API para el Meta-Agente.

Endpoints para generación de código de agentes:
- POST /generate - Generar código del agente
- POST /generate-stream - Generación con streaming
- GET /generated - Listar agentes generados
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.application.services.meta_agent import AgentPlan
from src.infrastructure.templates.agent_templates import AgentTemplate

router = APIRouter()


# ==================== Modelos de Request/Response ====================


class GenerateOptions(BaseModel):
    """Opciones para la generación de código."""

    include_comments: bool = Field(
        default=True, description="Incluir comentarios en el código"
    )
    add_examples: bool = Field(default=True, description="Añadir ejemplos de uso")
    save_to_file: bool = Field(
        default=True, description="Guardar automáticamente el archivo"
    )


class GenerateRequest(BaseModel):
    """Request para generar código de agente."""

    plan: AgentPlan = Field(description="Plan estructurado del agente")
    options: Optional[GenerateOptions] = Field(default_factory=GenerateOptions)


class GenerateResponse(BaseModel):
    """Response con el código generado."""

    code: str = Field(description="Código Python del agente")
    plan: AgentPlan = Field(description="Plan usado para generar")
    filename: str = Field(description="Nombre del archivo")
    filepath: str = Field(description="Ruta completa del archivo")
    lines: int = Field(description="Número de líneas de código")
    size_bytes: int = Field(description="Tamaño en bytes")
    created_at: str = Field(description="Timestamp de creación")


class GeneratedAgentInfo(BaseModel):
    """Información de un agente generado."""

    filename: str
    filepath: str
    plan_summary: Dict
    created_at: str
    size_bytes: int
    lines: int


class GeneratedAgentsResponse(BaseModel):
    """Response con lista de agentes generados."""

    agents: List[GeneratedAgentInfo]
    total: int
    output_dir: str


# ==================== Utilidades ====================


def get_output_dir() -> Path:
    """Retorna el directorio de salida para agentes generados."""
    output_dir = Path(os.getcwd()) / "generated" / "agents"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_filename(plan: AgentPlan) -> str:
    """Genera el nombre de archivo basado en el plan."""
    safe_name = plan.nombre.lower().replace(" ", "_").replace("-", "_")
    # Remover caracteres especiales
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
    return f"{safe_name}_agent.py"


def save_agent_file(plan: AgentPlan, code: str) -> tuple[str, str]:
    """
    Guarda el código del agente en un archivo.

    Returns:
        Tupla (filename, filepath)
    """
    output_dir = get_output_dir()
    filename = generate_filename(plan)
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    return filename, str(filepath)


# ==================== Endpoints ====================


@router.post("/generate", response_model=GenerateResponse)
async def generate_agent(req: GenerateRequest):
    """
    Generar código Python del agente basado en el plan.

    Este endpoint toma un AgentPlan y genera el código Python completo
    del agente usando las plantillas apropiadas según el nivel y configuración.
    """
    try:
        # Seleccionar template según el tipo de agente
        template = AgentTemplate()
        plan_dict = req.plan.model_dump()

        # Ajustar modelo si es necesario
        if req.plan.es_equipo and req.plan.modelo == "deepseek-chat":
            plan_dict["modelo"] = "deepseek-reasoner"

        # Generar código según el tipo
        if req.plan.es_equipo:
            code = template.generate_agent_team(plan_dict)
        elif req.plan.necesita_memoria or req.plan.nivel >= 3:
            code = template.generate_agent_with_memory(plan_dict)
        else:
            code = template.generate_basic_agent(plan_dict)

        # Guardar archivo si está configurado
        filename = ""
        filepath = ""
        if req.options.save_to_file:
            filename, filepath = save_agent_file(req.plan, code)
        else:
            filename = generate_filename(req.plan)
            filepath = str(get_output_dir() / filename)

        # Calcular métricas
        lines = len(code.split("\n"))
        size_bytes = len(code.encode("utf-8"))

        return GenerateResponse(
            code=code,
            plan=req.plan,
            filename=filename,
            filepath=filepath,
            lines=lines,
            size_bytes=size_bytes,
            created_at=datetime.now().isoformat(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al generar el agente: {str(e)}"
        )


@router.post("/generate-stream")
async def generate_agent_stream(req: GenerateRequest):
    """
    Generar código del agente con streaming de progreso.

    Retorna eventos SSE (Server-Sent Events) con el progreso:
    - start: Inicio de generación
    - progress: Progreso porcentual
    - code_chunk: Fragmento de código
    - complete: Generación completada
    - error: Error durante generación
    """

    async def event_generator():
        try:
            # Evento de inicio
            yield f"data: {json.dumps({'type': 'start', 'stage': 'analyzing'})}\n\n"
            await asyncio.sleep(0.3)

            # Preparar generación
            yield f"data: {json.dumps({'type': 'progress', 'stage': 'planning', 'percentage': 10})}\n\n"
            await asyncio.sleep(0.2)

            # Generar código
            template = AgentTemplate()
            plan_dict = req.plan.model_dump()

            if req.plan.es_equipo and req.plan.modelo == "deepseek-chat":
                plan_dict["modelo"] = "deepseek-reasoner"

            yield f"data: {json.dumps({'type': 'progress', 'stage': 'generating', 'percentage': 30})}\n\n"

            # Seleccionar y generar
            if req.plan.es_equipo:
                code = template.generate_agent_team(plan_dict)
            elif req.plan.necesita_memoria or req.plan.nivel >= 3:
                code = template.generate_agent_with_memory(plan_dict)
            else:
                code = template.generate_basic_agent(plan_dict)

            yield f"data: {json.dumps({'type': 'progress', 'stage': 'code_ready', 'percentage': 70})}\n\n"

            # Enviar código en chunks
            chunk_size = 500

            for index in range(0, len(code), chunk_size):
                chunk = code[index : index + chunk_size]
                yield f"data: {json.dumps({'type': 'code_chunk', 'content': chunk})}\n\n"

                # Progreso incremental
                progress = 70 + int((index / max(len(code), 1)) * 20)
                yield f"data: {json.dumps({'type': 'progress', 'percentage': progress})}\n\n"
                await asyncio.sleep(0.05)  # Simular trabajo

            # Guardar archivo
            if req.options.save_to_file:
                yield f"data: {json.dumps({'type': 'progress', 'stage': 'saving', 'percentage': 95})}\n\n"
                filename, filepath = save_agent_file(req.plan, code)
                await asyncio.sleep(0.2)
            else:
                filename = generate_filename(req.plan)
                filepath = str(get_output_dir() / filename)

            # Completado
            lines = len(code.split("\n"))
            yield f"data: {json.dumps({
                'type': 'complete',
                'filename': filename,
                'filepath': filepath,
                'lines': lines,
                'percentage': 100
            })}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.get("/generated", response_model=GeneratedAgentsResponse)
async def list_generated_agents(limit: int = 50, offset: int = 0):
    """
    Listar agentes generados.

    Retorna información de los archivos de agentes en el directorio generated/agents/
    """
    try:
        output_dir = get_output_dir()

        # Buscar archivos Python
        agent_files = sorted(
            output_dir.glob("*_agent.py"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,  # Más recientes primero
        )

        # Aplicar paginación
        total = len(agent_files)
        agent_files = agent_files[offset : offset + limit]

        # Recopilar información
        agents_info = []
        for filepath in agent_files:
            stat = filepath.stat()

            # Leer primeras líneas para extraer info del docstring
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                    # Extraer nombre y rol del docstring
                    nombre = (
                        filepath.stem.replace("_agent", "").replace("_", " ").title()
                    )
                    rol = "Agente AI"

                    # Buscar info en el docstring
                    in_docstring = False
                    for line in lines[:20]:
                        if '"""' in line:
                            in_docstring = not in_docstring
                            continue
                        if in_docstring and "Rol:" in line:
                            rol = line.split("Rol:")[1].strip()
                            break

                    plan_summary = {
                        "nombre": nombre,
                        "rol": rol,
                    }
            except Exception:
                plan_summary = {"nombre": filepath.stem, "rol": "Unknown"}

            agents_info.append(
                GeneratedAgentInfo(
                    filename=filepath.name,
                    filepath=str(filepath),
                    plan_summary=plan_summary,
                    created_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    size_bytes=stat.st_size,
                    lines=len(content.split("\n")) if "content" in locals() else 0,
                )
            )

        return GeneratedAgentsResponse(
            agents=agents_info,
            total=total,
            output_dir=str(output_dir),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al listar agentes: {str(e)}"
        )


@router.get("/health")
async def meta_agent_health():
    """Health check del módulo Meta-Agent."""
    return {
        "status": "ok",
        "service": "meta-agent-api",
        "version": "1.0.0",
        "output_dir": str(get_output_dir()),
    }
