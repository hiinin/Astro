from fastapi import APIRouter, Request

from core.config import EONET
from core.proxy import proxy

router = APIRouter(prefix="/eonet", tags=["EONET – Eventos Naturais da Terra"])


@router.get("/events")
async def eonet_events(request: Request):
    return await proxy(f"{EONET}/events", dict(request.query_params))


@router.get("/events/{event_id}")
async def eonet_event_by_id(event_id: str):
    return await proxy(f"{EONET}/events/{event_id}")


@router.get("/categories")
async def eonet_categories():
    return await proxy(f"{EONET}/categories")


@router.get("/categories/{category_id}")
async def eonet_events_by_category(category_id: str, request: Request):
    return await proxy(f"{EONET}/categories/{category_id}", dict(request.query_params))


@router.get("/layers")
async def eonet_layers():
    return await proxy(f"{EONET}/layers")


@router.get("/layers/{category_id}")
async def eonet_layers_by_category(category_id: str):
    return await proxy(f"{EONET}/layers/{category_id}")
