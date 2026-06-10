from fastapi import APIRouter, Request

from core.config import DONKI
from core.proxy import proxy

router = APIRouter(prefix="/donki", tags=["DONKI – Clima Espacial"])


@router.get("/cme")
async def donki_cme(request: Request):
    return await proxy(f"{DONKI}/CME", dict(request.query_params))


@router.get("/cme-analysis")
async def donki_cme_analysis(request: Request):
    return await proxy(f"{DONKI}/CMEAnalysis", dict(request.query_params))


@router.get("/gst")
async def donki_gst(request: Request):
    return await proxy(f"{DONKI}/GST", dict(request.query_params))


@router.get("/ips")
async def donki_ips(request: Request):
    return await proxy(f"{DONKI}/IPS", dict(request.query_params))


@router.get("/flr")
async def donki_flr(request: Request):
    return await proxy(f"{DONKI}/FLR", dict(request.query_params))


@router.get("/sep")
async def donki_sep(request: Request):
    return await proxy(f"{DONKI}/SEP", dict(request.query_params))


@router.get("/mpc")
async def donki_mpc(request: Request):
    return await proxy(f"{DONKI}/MPC", dict(request.query_params))


@router.get("/rbe")
async def donki_rbe(request: Request):
    return await proxy(f"{DONKI}/RBE", dict(request.query_params))


@router.get("/hss")
async def donki_hss(request: Request):
    return await proxy(f"{DONKI}/HSS", dict(request.query_params))


@router.get("/wsa-enlil")
async def donki_wsa_enlil(request: Request):
    return await proxy(f"{DONKI}/WSAEnlilSimulations", dict(request.query_params))


@router.get("/notifications")
async def donki_notifications(request: Request):
    return await proxy(f"{DONKI}/notifications", dict(request.query_params))
