from fastapi import APIRouter, Request

from core.config import IMAGES
from core.proxy import proxy

router = APIRouter(prefix="/images", tags=["NASA Image & Video Library"])


@router.get("/search")
async def images_search(request: Request):
    return await proxy(f"{IMAGES}/search", dict(request.query_params))


@router.get("/asset/{nasa_id}")
async def images_asset(nasa_id: str):
    return await proxy(f"{IMAGES}/asset/{nasa_id}")


@router.get("/metadata/{nasa_id}")
async def images_metadata(nasa_id: str):
    return await proxy(f"{IMAGES}/metadata/{nasa_id}")


@router.get("/captions/{nasa_id}")
async def images_captions(nasa_id: str):
    return await proxy(f"{IMAGES}/captions/{nasa_id}")


@router.get("/album/{album_name}")
async def images_album(album_name: str):
    return await proxy(f"{IMAGES}/album/{album_name}")
