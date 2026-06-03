from fastapi import APIRouter, Request

from core.config import API_KEY, NASA
from core.proxy import proxy

router = APIRouter(prefix="/donki", tags=["DONKI – Clima Espacial"])


@router.get("/cme")
async def donki_cme(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/CME", params)


@router.get("/cme-analysis")
async def donki_cme_analysis(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/CMEAnalysis", params)


@router.get("/gst")
async def donki_gst(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/GST", params)


@router.get("/ips")
async def donki_ips(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/IPS", params)


@router.get("/flr")
async def donki_flr(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/FLR", params)


@router.get("/sep")
async def donki_sep(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/SEP", params)


@router.get("/mpc")
async def donki_mpc(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/MPC", params)


@router.get("/rbe")
async def donki_rbe(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/RBE", params)


@router.get("/hss")
async def donki_hss(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/HSS", params)


@router.get("/wsa-enlil")
async def donki_wsa_enlil(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/WSAEnlilSimulations", params)


@router.get("/notifications")
async def donki_notifications(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/notifications", params)
