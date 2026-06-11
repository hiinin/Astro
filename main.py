from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.proxy import close_client, init_client
from routers import (
    foto_do_dia,
    asteroides,
    clima_espacial,
    camera_terra,
    clima_marte,
    rovers_marte,
    midias,
    sistema_solar,
    eventos_naturais,
    satelites,
    exoplanetas,
    ciencia_aberta,
    imagens_terra,
    projetos,
    techtransfer,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_client()
    yield
    await close_client()


app = FastAPI(
    title="Astro – NASA API Proxy",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(foto_do_dia.router)
app.include_router(asteroides.router)
app.include_router(clima_espacial.router)
app.include_router(camera_terra.router)
app.include_router(clima_marte.router)
app.include_router(rovers_marte.router)
app.include_router(midias.router)
app.include_router(sistema_solar.router)
app.include_router(eventos_naturais.router)
app.include_router(satelites.router)
app.include_router(exoplanetas.router)
app.include_router(ciencia_aberta.router)
app.include_router(imagens_terra.router)
app.include_router(projetos.router)
app.include_router(techtransfer.router)
