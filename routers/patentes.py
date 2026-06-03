from fastapi import APIRouter, Request

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/techtransfer", tags=["TechTransfer – Patentes e Spinoffs"])


@router.get("/patent")
async def techtransfer_patent(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/patent/", params)


@router.get("/patent-issued")
async def techtransfer_patent_issued(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/patent_issued/", params)


@router.get("/software")
async def techtransfer_software(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/software/", params)


@router.get("/spinoff")
async def techtransfer_spinoff(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/spinoff/", params)
