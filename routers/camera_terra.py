from fastapi import APIRouter

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/epic", tags=["EPIC – Câmera da Terra (DSCOVR)"])


@router.get("/natural")
async def epic_natural():
    return await proxy(f"{NASA}/EPIC/api/natural", {"api_key": API_KEY})


@router.get("/natural/all")
async def epic_natural_all():
    return await proxy(f"{NASA}/EPIC/api/natural/all", {"api_key": API_KEY})


@router.get("/natural/available")
async def epic_natural_available():
    return await proxy(f"{NASA}/EPIC/api/natural/available", {"api_key": API_KEY})


@router.get("/natural/date/{date}")
async def epic_natural_date(date: str):
    return await proxy(f"{NASA}/EPIC/api/natural/date/{date}", {"api_key": API_KEY})


@router.get("/enhanced")
async def epic_enhanced():
    return await proxy(f"{NASA}/EPIC/api/enhanced", {"api_key": API_KEY})


@router.get("/enhanced/all")
async def epic_enhanced_all():
    return await proxy(f"{NASA}/EPIC/api/enhanced/all", {"api_key": API_KEY})


@router.get("/enhanced/available")
async def epic_enhanced_available():
    return await proxy(f"{NASA}/EPIC/api/enhanced/available", {"api_key": API_KEY})


@router.get("/enhanced/date/{date}")
async def epic_enhanced_date(date: str):
    return await proxy(f"{NASA}/EPIC/api/enhanced/date/{date}", {"api_key": API_KEY})
