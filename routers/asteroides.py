from fastapi import APIRouter

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/neo", tags=["NeoWs – Asteroides"])


@router.get("/browse")
async def neo_browse(page: int = 0):
    return await proxy(f"{NASA}/neo/rest/v1/neo/browse", {"api_key": API_KEY, "page": page})


@router.get("/lookup/{asteroid_id}")
async def neo_lookup(asteroid_id: int):
    return await proxy(f"{NASA}/neo/rest/v1/neo/{asteroid_id}", {"api_key": API_KEY})
