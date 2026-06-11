from datetime import date, timedelta

from fastapi import APIRouter, Query

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/neo", tags=["NeoWs – Asteroides"])


@router.get("/feed")
async def neo_feed(
    start_date: str | None = Query(
        None,
        description="Data inicial da busca (YYYY-MM-DD). Default: 7 dias atrás.",
    ),
    end_date: str | None = Query(
        None,
        description="Data final da busca (YYYY-MM-DD). Default: hoje.",
    ),
):
    end = end_date or date.today().isoformat()
    start = start_date or (date.today() - timedelta(days=7)).isoformat()
    return await proxy(f"{NASA}/neo/rest/v1/feed", {"api_key": API_KEY, "start_date": start, "end_date": end})


@router.get("/browse")
async def neo_browse(page: int = 0):
    return await proxy(f"{NASA}/neo/rest/v1/neo/browse", {"api_key": API_KEY, "page": page})


@router.get("/lookup/{asteroid_id}")
async def neo_lookup(asteroid_id: int):
    return await proxy(f"{NASA}/neo/rest/v1/neo/{asteroid_id}", {"api_key": API_KEY})


@router.get("/stats")
async def neo_stats():
    return await proxy(f"{NASA}/neo/rest/v1/neo/stats", {"api_key": API_KEY})
