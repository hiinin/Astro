from fastapi import APIRouter, HTTPException, Query

from core.config import CELESTRAK
from core.proxy import proxy

router = APIRouter(prefix="/tle", tags=["TLE – Elementos Orbitais de Satélites"])


@router.get("")
async def tle_search(search: str = Query(..., min_length=1)):
    return await proxy(CELESTRAK, {"NAME": search, "FORMAT": "JSON"})


@router.get("/{satellite_id}")
async def tle_by_id(satellite_id: int):
    data = await proxy(CELESTRAK, {"CATNR": satellite_id, "FORMAT": "JSON"})
    if not data:
        raise HTTPException(status_code=404, detail="Satélite não encontrado.")
    return data[0]
