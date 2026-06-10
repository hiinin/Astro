from datetime import date as dt_date, timedelta
from urllib.parse import urlencode

from fastapi import APIRouter, Query

from core.config import GIBS_LAYER, GIBS_WMS

router = APIRouter(prefix="/earth", tags=["Earth – Imagens via GIBS"])

DEFAULT_OFFSET_DAYS = 2
MAX_RETRY_DAYS = 14


def _default_date() -> str:
    return (dt_date.today() - timedelta(days=DEFAULT_OFFSET_DAYS)).isoformat()


def _bbox(lon: float, lat: float, dim: float) -> str:
    half = dim / 2
    return f"{lon - half},{lat - half},{lon + half},{lat + half}"


def _gibs_url(lon: float, lat: float, dim: float, date: str) -> str:
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.1.1",
        "REQUEST": "GetMap",
        "LAYERS": GIBS_LAYER,
        "BBOX": _bbox(lon, lat, dim),
        "WIDTH": "512",
        "HEIGHT": "512",
        "SRS": "EPSG:4326",
        "FORMAT": "image/jpeg",
        "TIME": date,
    }
    return f"{GIBS_WMS}?{urlencode(params)}"


@router.get("/imagery")
async def earth_imagery(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    dim: float = Query(0.1, gt=0, le=1),
    date: str | None = Query(None, description="ISO date (YYYY-MM-DD); default: 2 days ago"),
):
    imagery_date = date or _default_date()
    return {
        "date": imagery_date,
        "layer": GIBS_LAYER,
        "lat": lat,
        "lon": lon,
        "dim": dim,
        "url": _gibs_url(lon, lat, dim, imagery_date),
    }


@router.get("/assets")
async def earth_assets(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    today = dt_date.today()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(DEFAULT_OFFSET_DAYS, DEFAULT_OFFSET_DAYS + MAX_RETRY_DAYS)]
    return {"lat": lat, "lon": lon, "dates": dates}