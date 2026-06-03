from fastapi import APIRouter, Request

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/earth", tags=["Earth – Imagens Landsat 8"])


@router.get("/imagery")
async def earth_imagery(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/earth/imagery", params)


@router.get("/assets")
async def earth_assets(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/earth/assets", params)
