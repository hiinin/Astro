from fastapi import APIRouter, Request

from core.config import MARS_ROVERS
from core.proxy import proxy

router = APIRouter(prefix="/mars-rovers", tags=["Mars Rovers – Fotos de Marte"])


@router.get("/{rover}/photos")
async def mars_rover_photos(rover: str, request: Request):
    return await proxy(
        f"{MARS_ROVERS}/rovers/{rover}/photos",
        dict(request.query_params),
    )


@router.get("/{rover}/latest-photos")
async def mars_rover_latest_photos(rover: str, request: Request):
    return await proxy(
        f"{MARS_ROVERS}/rovers/{rover}/latest_photos",
        dict(request.query_params),
    )


@router.get("/{rover}/manifesto")
async def mars_rover_manifesto(rover: str):
    return await proxy(f"{MARS_ROVERS}/manifests/{rover}")
