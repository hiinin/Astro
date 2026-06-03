from fastapi import APIRouter, Request

from core.config import TLE
from core.proxy import proxy

router = APIRouter(prefix="/tle", tags=["TLE – Elementos Orbitais de Satélites"])


@router.get("")
async def tle_search(request: Request):
    return await proxy(TLE, dict(request.query_params))


@router.get("/{satellite_id}")
async def tle_by_id(satellite_id: int):
    return await proxy(f"{TLE}/{satellite_id}")
