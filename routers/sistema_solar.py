from fastapi import APIRouter, Request

from core.config import SSD
from core.proxy import proxy

router = APIRouter(prefix="/ssd", tags=["SSD/CNEOS – Sistema Solar e NEOs"])


@router.get("/cad")
async def ssd_cad(request: Request):
    return await proxy(f"{SSD}/cad.api", dict(request.query_params))


@router.get("/fireball")
async def ssd_fireball(request: Request):
    return await proxy(f"{SSD}/fireball.api", dict(request.query_params))


@router.get("/nhats")
async def ssd_nhats(request: Request):
    return await proxy(f"{SSD}/nhats.api", dict(request.query_params))


@router.get("/scout")
async def ssd_scout(request: Request):
    return await proxy(f"{SSD}/scout.api", dict(request.query_params))


@router.get("/sentry")
async def ssd_sentry(request: Request):
    return await proxy(f"{SSD}/sentry.api", dict(request.query_params))
