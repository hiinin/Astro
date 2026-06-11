from fastapi import APIRouter, Query

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/apod", tags=["APOD"])


@router.get("")
async def apod(
    date: str | None = Query(None, description="Data da foto (YYYY-MM-DD). Default: hoje."),
    thumbs: bool = Query(False, description="Incluir URL de thumbnail para vídeos."),
):
    params = {"api_key": API_KEY}
    if date:
        params["date"] = date
    if thumbs:
        params["thumbs"] = "true"
    return await proxy(f"{NASA}/planetary/apod", params)
