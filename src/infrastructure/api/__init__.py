"""
Módulo de API para AgentOS.

Contiene las rutas custom del Meta-Agente para generación de código.
"""

from .meta_routes import router as meta_router

__all__ = ["meta_router"]

