from fastapi import APIRouter, Request

from core.config import TECHPORT
from core.proxy import proxy

router = APIRouter(prefix="/techport", tags=["Techport – Portfólio de Tecnologia"])


@router.get("/projects")
async def techport_projects(request: Request):
    return await proxy(f"{TECHPORT}/projects", dict(request.query_params))


@router.get("/projects/{project_id}")
async def techport_project(project_id: int):
    return await proxy(f"{TECHPORT}/projects/{project_id}")
