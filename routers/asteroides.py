from fastapi import APIRouter, Request

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/neo", tags=["NeoWs – Asteroides"])


@router.get("/feed")
async def neo_feed(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/neo/rest/v1/feed", params)


@router.get("/browse")
async def neo_browse():
    return await proxy(f"{NASA}/neo/rest/v1/neo/browse", {"api_key": API_KEY})


@router.get("/lookup/{asteroid_id}")
async def neo_lookup(asteroid_id: int):
    return await proxy(f"{NASA}/neo/rest/v1/neo/{asteroid_id}", {"api_key": API_KEY})
