from fastapi import APIRouter, Request

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/insight", tags=["InSight – Clima em Marte"])


@router.get("/weather")
async def insight_weather(request: Request):
    params = {"api_key": API_KEY, "feedtype": "json", "ver": "1.0", **request.query_params}
    return await proxy(f"{NASA}/insight_weather/", params)
