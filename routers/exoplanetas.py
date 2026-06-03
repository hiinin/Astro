from fastapi import APIRouter, Request

from core.config import EXO
from core.proxy import proxy

router = APIRouter(prefix="/exoplanet", tags=["Exoplanet Archive"])


@router.get("")
async def exoplanet(request: Request):
    params = {"format": "json", **request.query_params}
    return await proxy(EXO, params)
