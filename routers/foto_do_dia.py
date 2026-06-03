from fastapi import APIRouter, Request

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/apod", tags=["APOD"])


@router.get("")
async def apod(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/apod", params)
