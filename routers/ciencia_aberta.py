from fastapi import APIRouter, Request

from core.config import OSDR
from core.proxy import proxy

router = APIRouter(prefix="/osdr", tags=["OSDR – Repositório de Ciência Aberta"])


@router.get("/study/files/{study_ids}")
async def osdr_study_files(study_ids: str, request: Request):
    return await proxy(f"{OSDR}/osdr/data/osd/files/{study_ids}", dict(request.query_params))


@router.get("/study/meta/{study_id}")
async def osdr_study_meta(study_id: int):
    return await proxy(f"{OSDR}/osdr/data/osd/meta/{study_id}")


@router.get("/search")
async def osdr_search(request: Request):
    return await proxy(f"{OSDR}/osdr/data/search", dict(request.query_params))


@router.get("/experiments")
async def osdr_experiments():
    return await proxy(f"{OSDR}/geode-py/ws/api/experiments")


@router.get("/experiment/{identifier}")
async def osdr_experiment(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/experiment/{identifier}")


@router.get("/missions")
async def osdr_missions():
    return await proxy(f"{OSDR}/geode-py/ws/api/missions")


@router.get("/mission/{identifier}")
async def osdr_mission(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/mission/{identifier}")


@router.get("/payloads")
async def osdr_payloads():
    return await proxy(f"{OSDR}/geode-py/ws/api/payloads")


@router.get("/payload/{identifier}")
async def osdr_payload(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/payload/{identifier}")


@router.get("/hardware")
async def osdr_hardware():
    return await proxy(f"{OSDR}/geode-py/ws/api/hardware")


@router.get("/hardware/{identifier}")
async def osdr_hardware_by_id(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/hardware/{identifier}")


@router.get("/vehicles")
async def osdr_vehicles():
    return await proxy(f"{OSDR}/geode-py/ws/api/vehicles")


@router.get("/vehicle/{identifier}")
async def osdr_vehicle(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/vehicle/{identifier}")


@router.get("/subjects")
async def osdr_subjects():
    return await proxy(f"{OSDR}/geode-py/ws/api/subjects")


@router.get("/subject/{identifier}")
async def osdr_subject(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/subject/{identifier}")


@router.get("/biospecimens")
async def osdr_biospecimens():
    return await proxy(f"{OSDR}/geode-py/ws/api/biospecimens")


@router.get("/biospecimen/{identifier}")
async def osdr_biospecimen(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/biospecimen/{identifier}")
