from fastapi import APIRouter, Request

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/mars-rovers", tags=["Mars Rovers – Fotos de Marte"])


@router.get("/{rover}/photos")
async def mars_rover_photos(rover: str, request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/mars-photos/api/v1/rovers/{rover}/photos", params)


@router.get("/{rover}/manifesto")
async def mars_rover_manifesto(rover: str):
    return await proxy(f"{NASA}/mars-photos/api/v1/manifests/{rover}", {"api_key": API_KEY})
