from fastapi import APIRouter

from core.proxy import proxy

TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

router = APIRouter(prefix="/exoplanet", tags=["Exoplanet Archive"])


@router.get("")
async def exoplanet():
    return await proxy(TAP, {
        "QUERY": "select pl_name,hostname,disc_year,discoverymethod,pl_orbper,pl_rade,pl_bmasse,sy_dist from pscomppars",
        "FORMAT": "json",
        "MAXREC": "200",
    })
