from urllib.parse import quote

from fastapi import APIRouter, Query

from core.config import TECHTRANSFER
from core.proxy import proxy

router = APIRouter(prefix="/techtransfer", tags=["TechTransfer"])


@router.get("/patent")
async def techtransfer_patent(patent: str = Query(..., min_length=1)):
    return await proxy(f"{TECHTRANSFER}/patent/{quote(patent.strip())}")


@router.get("/software")
async def techtransfer_software(software: str = Query(..., min_length=1)):
    return await proxy(f"{TECHTRANSFER}/software/{quote(software.strip())}")


@router.get("/spinoff")
async def techtransfer_spinoff(spinoff: str = Query(..., min_length=1)):
    return await proxy(f"{TECHTRANSFER}/spinoff/{quote(spinoff.strip())}")
