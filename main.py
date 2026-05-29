from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(
    title="NASA API Proxy",
    version="1.0.0",
)

API_KEY = "DEMO_KEY"  # Substitua pela sua chave em api.nasa.gov

# URLs base de cada serviço da NASA
NASA    = "https://api.nasa.gov"                                                      # API principal da NASA
IMAGES  = "https://images-api.nasa.gov"                                               # Biblioteca de imagens e vídeos
SSD     = "https://ssd-api.jpl.nasa.gov"                                              # Dinâmica do Sistema Solar (JPL)
EONET   = "https://eonet.gsfc.nasa.gov/api/v3"                                        # Eventos naturais da Terra
TLE     = "https://tle.ivanstanojevic.me/api/tle"                                     # Elementos orbitais de satélites
EXO     = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"   # Arquivo de exoplanetas
OSDR    = "https://osdr.nasa.gov"                                                     # Repositório de ciência aberta


# Função auxiliar que faz a requisição GET e retorna o JSON da resposta
async def proxy(url: str, params: dict = {}) -> JSONResponse:
    async with httpx.AsyncClient() as c:
        r = await c.get(url, params=params)
        return r.json()


# ── Earth - Imagens Landsat 8 de pontos geográficos ──────────────────────────

# Retorna a imagem de satélite Landsat 8 de uma coordenada geográfica
# Parâmetros obrigatórios: lat (latitude), lon (longitude)
# Parâmetros opcionais: date (YYYY-MM-DD), dim (graus de largura da imagem, padrão 0.025)
@app.get("/earth/imagery")
async def earth_imagery(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/earth/imagery", params)

# Retorna os metadados e URL da imagem Landsat mais próxima de uma data
# Parâmetros obrigatórios: lat (latitude), lon (longitude)
# Parâmetros opcionais: date (YYYY-MM-DD), dim (graus de largura)
@app.get("/earth/assets")
async def earth_assets(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/earth/assets", params)


# ── APOD - Imagem Astronômica do Dia ──────────────────────────────────────────
# Parâmetros aceitos: date (YYYY-MM-DD), start_date, end_date, count, thumbs, hd

@app.get("/apod")
async def apod(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/apod", params)


# ── NeoWs - Asteroides Próximos da Terra ──────────────────────────────────────

# Lista asteroides por intervalo de datas de aproximação à Terra
# Parâmetros: start_date (YYYY-MM-DD), end_date (máx 7 dias após start_date)
@app.get("/neo/feed")
async def neo_feed(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/neo/rest/v1/feed", params)

# Navega pelo dataset completo de asteroides (paginado)
@app.get("/neo/browse")
async def neo_browse():
    return await proxy(f"{NASA}/neo/rest/v1/neo/browse", {"api_key": API_KEY})

# Busca um asteroide específico pelo ID SPK do NASA JPL
@app.get("/neo/lookup/{asteroid_id}")
async def neo_lookup(asteroid_id: int):
    return await proxy(f"{NASA}/neo/rest/v1/neo/{asteroid_id}", {"api_key": API_KEY})


# ── DONKI - Banco de Dados de Clima Espacial ──────────────────────────────────
# Todos os endpoints aceitam: startDate e endDate (YYYY-MM-DD)

# Ejeção de Massa Coronal
@app.get("/donki/cme")
async def donki_cme(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/CME", params)

# Análise de Ejeção de Massa Coronal
# Parâmetros extras: mostAccurateOnly, speed, halfAngle, catalog (ALL | SWRC_CATALOG | JANG_ET_AL_CATALOG)
@app.get("/donki/cme-analysis")
async def donki_cme_analysis(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/CMEAnalysis", params)

# Tempestade Geomagnética
@app.get("/donki/gst")
async def donki_gst(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/GST", params)

# Choque Interplanetário
# Parâmetros extras: location (ALL | Earth | MESSENGER | STEREO A | STEREO B), catalog
@app.get("/donki/ips")
async def donki_ips(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/IPS", params)

# Explosão Solar
@app.get("/donki/flr")
async def donki_flr(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/FLR", params)

# Partícula Solar Energética
@app.get("/donki/sep")
async def donki_sep(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/SEP", params)

# Cruzamento da Magnetopausa
@app.get("/donki/mpc")
async def donki_mpc(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/MPC", params)

# Aumento do Cinturão de Radiação
@app.get("/donki/rbe")
async def donki_rbe(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/RBE", params)

# Corrente de Alta Velocidade
@app.get("/donki/hss")
async def donki_hss(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/HSS", params)

# Simulação WSA+Enlil (modelo de propagação do vento solar)
@app.get("/donki/wsa-enlil")
async def donki_wsa_enlil(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/WSAEnlilSimulations", params)

# Notificações de clima espacial
# Parâmetro extra: type (all | FLR | SEP | CME | IPS | MPC | GST | RBE | report)
@app.get("/donki/notifications")
async def donki_notifications(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/notifications", params)


# ── EPIC - Câmera de Imagem Policromática da Terra (satélite DSCOVR) ──────────

# Imagem natural mais recente da Terra (cor real)
@app.get("/epic/natural")
async def epic_natural():
    return await proxy(f"{NASA}/EPIC/api/natural", {"api_key": API_KEY})

# Todas as datas com imagens naturais disponíveis
@app.get("/epic/natural/all")
async def epic_natural_all():
    return await proxy(f"{NASA}/EPIC/api/natural/all", {"api_key": API_KEY})

# Datas disponíveis (formato alternativo)
@app.get("/epic/natural/available")
async def epic_natural_available():
    return await proxy(f"{NASA}/EPIC/api/natural/available", {"api_key": API_KEY})

# Imagens naturais de uma data específica (YYYY-MM-DD)
@app.get("/epic/natural/date/{date}")
async def epic_natural_date(date: str):
    return await proxy(f"{NASA}/EPIC/api/natural/date/{date}", {"api_key": API_KEY})

# Imagem aprimorada mais recente (cores intensificadas para análise científica)
@app.get("/epic/enhanced")
async def epic_enhanced():
    return await proxy(f"{NASA}/EPIC/api/enhanced", {"api_key": API_KEY})

# Todas as datas com imagens aprimoradas disponíveis
@app.get("/epic/enhanced/all")
async def epic_enhanced_all():
    return await proxy(f"{NASA}/EPIC/api/enhanced/all", {"api_key": API_KEY})

# Datas disponíveis para imagens aprimoradas (formato alternativo)
@app.get("/epic/enhanced/available")
async def epic_enhanced_available():
    return await proxy(f"{NASA}/EPIC/api/enhanced/available", {"api_key": API_KEY})

# Imagens aprimoradas de uma data específica (YYYY-MM-DD)
@app.get("/epic/enhanced/date/{date}")
async def epic_enhanced_date(date: str):
    return await proxy(f"{NASA}/EPIC/api/enhanced/date/{date}", {"api_key": API_KEY})


# ── InSight - Clima em Marte ───────────────────────────────────────────────────
# Retorna dados dos últimos 7 Sols (dias marcianos): temperatura, vento, pressão
# Parâmetros: feedtype (json), ver (1.0)

@app.get("/insight/weather")
async def insight_weather(request: Request):
    params = {"api_key": API_KEY, "feedtype": "json", "ver": "1.0", **request.query_params}
    return await proxy(f"{NASA}/insight_weather/", params)


# ── Mars Rover Photos - Fotos dos Rovers em Marte ─────────────────────────────

# Fotos de um rover por sol marciano ou data terrestre
# rover: curiosity | opportunity | spirit | perseverance
# Parâmetros: sol (dia marciano), earth_date (YYYY-MM-DD), camera, page
@app.get("/mars-rovers/{rover}/photos")
async def mars_rover_photos(rover: str, request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/mars-photos/api/v1/rovers/{rover}/photos", params)

# Manifesto da missão: datas, total de fotos, status e câmeras disponíveis
@app.get("/mars-rovers/{rover}/manifesto")
async def mars_rover_manifesto(rover: str):
    return await proxy(f"{NASA}/mars-photos/api/v1/manifests/{rover}", {"api_key": API_KEY})


# ── NASA Image & Video Library - Acervo de Mídia da NASA ──────────────────────

# Busca no acervo por termo
# Parâmetros: q (obrigatório), media_type (image | video | audio), year_start, year_end, page
@app.get("/images/search")
async def images_search(request: Request):
    return await proxy(f"{IMAGES}/search", dict(request.query_params))

# Manifesto de um ativo de mídia (lista de URLs do arquivo)
@app.get("/images/asset/{nasa_id}")
async def images_asset(nasa_id: str):
    return await proxy(f"{IMAGES}/asset/{nasa_id}")

# Localização dos metadados de um ativo de mídia
@app.get("/images/metadata/{nasa_id}")
async def images_metadata(nasa_id: str):
    return await proxy(f"{IMAGES}/metadata/{nasa_id}")

# Localização do arquivo de legendas de um vídeo
@app.get("/images/captions/{nasa_id}")
async def images_captions(nasa_id: str):
    return await proxy(f"{IMAGES}/captions/{nasa_id}")

# Conteúdo de um álbum de mídia
@app.get("/images/album/{album_name}")
async def images_album(album_name: str):
    return await proxy(f"{IMAGES}/album/{album_name}")


# ── TechTransfer - Patentes, Software e Spinoffs da NASA ──────────────────────

# Busca patentes pelo termo (ex: ?patent=engine)
@app.get("/techtransfer/patent")
async def techtransfer_patent(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/patent/", params)

# Busca patentes emitidas pelo termo (ex: ?patent_issued=propulsion)
@app.get("/techtransfer/patent-issued")
async def techtransfer_patent_issued(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/patent_issued/", params)

# Busca software open-source da NASA (ex: ?software=satellite)
@app.get("/techtransfer/software")
async def techtransfer_software(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/software/", params)

# Busca exemplos de tecnologia transferida ao setor privado (ex: ?spinoff=medical)
@app.get("/techtransfer/spinoff")
async def techtransfer_spinoff(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/spinoff/", params)


# ── SSD/CNEOS - Dinâmica do Sistema Solar e Objetos Próximos da Terra ─────────

# Dados de aproximação de asteroides e cometas aos planetas
# Parâmetros: date-min, date-max, dist-max (ex: 0.05 AU), neo (true/false)
@app.get("/ssd/cad")
async def ssd_cad(request: Request):
    return await proxy(f"{SSD}/cad.api", dict(request.query_params))

# Bolas de fogo (meteoros) detectadas por sensores do governo americano
# Parâmetros: date-min, date-max, energy-min (kt), req-loc (true/false)
@app.get("/ssd/fireball")
async def ssd_fireball(request: Request):
    return await proxy(f"{SSD}/fireball.api", dict(request.query_params))

# NEOs acessíveis para missões humanas (NHATS)
# Parâmetros: dv (delta-v em km/s), dur (duração em dias), stay, launch (ex: 2020-2025)
@app.get("/ssd/nhats")
async def ssd_nhats(request: Request):
    return await proxy(f"{SSD}/nhats.api", dict(request.query_params))

# Dados em tempo real do sistema Scout (risco de impacto de objetos recém-descobertos)
# Parâmetros: tdes (designação temporária do objeto)
@app.get("/ssd/scout")
async def ssd_scout(request: Request):
    return await proxy(f"{SSD}/scout.api", dict(request.query_params))

# Avaliação de risco de impacto de NEOs na Terra (sistema Sentry)
# Parâmetros: spk (ID do objeto), des (designação), removed (objetos removidos da lista)
@app.get("/ssd/sentry")
async def ssd_sentry(request: Request):
    return await proxy(f"{SSD}/sentry.api", dict(request.query_params))


# ── EONET - Rastreador de Eventos Naturais da Terra ───────────────────────────

# Lista eventos naturais ativos ou encerrados (furacões, incêndios, vulcões etc.)
# Parâmetros: status (open | closed), limit, days, source, category, bbox
@app.get("/eonet/events")
async def eonet_events(request: Request):
    return await proxy(f"{EONET}/events", dict(request.query_params))

# Detalhes de um evento específico pelo ID
@app.get("/eonet/events/{event_id}")
async def eonet_event_by_id(event_id: str):
    return await proxy(f"{EONET}/events/{event_id}")

# Lista todas as categorias de eventos (wildfires, volcanoes, storms etc.)
@app.get("/eonet/categories")
async def eonet_categories():
    return await proxy(f"{EONET}/categories")

# Eventos filtrados por categoria
# Parâmetros: status, limit, days
@app.get("/eonet/categories/{category_id}")
async def eonet_events_by_category(category_id: str, request: Request):
    return await proxy(f"{EONET}/categories/{category_id}", dict(request.query_params))

# Camadas de imagens de satélite vinculadas a categorias de eventos
@app.get("/eonet/layers")
async def eonet_layers():
    return await proxy(f"{EONET}/layers")

# Camadas de imagens filtradas por categoria
@app.get("/eonet/layers/{category_id}")
async def eonet_layers_by_category(category_id: str):
    return await proxy(f"{EONET}/layers/{category_id}")


# ── TLE API - Elementos Orbitais de Satélites ─────────────────────────────────

# Busca satélites pelo nome (ex: ?search=ISS)
@app.get("/tle")
async def tle_search(request: Request):
    return await proxy(TLE, dict(request.query_params))

# Retorna o TLE de um satélite pelo número NORAD (ex: 25544 = ISS)
@app.get("/tle/{satellite_id}")
async def tle_by_id(satellite_id: int):
    return await proxy(f"{TLE}/{satellite_id}")


# ── Exoplanet Archive - Arquivo de Exoplanetas da NASA ────────────────────────
# Parâmetros: table (exoplanets | cumulative | ...), select (colunas), where (filtro SQL), format (json | csv)

@app.get("/exoplanet")
async def exoplanet(request: Request):
    params = {"format": "json", **request.query_params}
    return await proxy(EXO, params)


# ── OSDR - Repositório de Ciência Aberta da NASA ──────────────────────────────

# Arquivos de um estudo OSD (ex: /osdr/study/files/87)
# Parâmetros: page, size
@app.get("/osdr/study/files/{study_ids}")
async def osdr_study_files(study_ids: str, request: Request):
    return await proxy(f"{OSDR}/osdr/data/osd/files/{study_ids}", dict(request.query_params))

# Metadados completos de um estudo OSD
@app.get("/osdr/study/meta/{study_id}")
async def osdr_study_meta(study_id: int):
    return await proxy(f"{OSDR}/osdr/data/osd/meta/{study_id}")

# Busca datasets por palavra-chave
# Parâmetros: term, from, size, type (cgene | nih_geo_gse | ebi_pride | mg_rast)
@app.get("/osdr/search")
async def osdr_search(request: Request):
    return await proxy(f"{OSDR}/osdr/data/search", dict(request.query_params))

# Lista todos os experimentos cadastrados
@app.get("/osdr/experiments")
async def osdr_experiments():
    return await proxy(f"{OSDR}/geode-py/ws/api/experiments")

# Detalhes de um experimento pelo identificador
@app.get("/osdr/experiment/{identifier}")
async def osdr_experiment(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/experiment/{identifier}")

# Lista todas as missões espaciais cadastradas
@app.get("/osdr/missions")
async def osdr_missions():
    return await proxy(f"{OSDR}/geode-py/ws/api/missions")

# Detalhes de uma missão pelo identificador (ex: SpaceX-12)
@app.get("/osdr/mission/{identifier}")
async def osdr_mission(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/mission/{identifier}")

# Lista todos os payloads (cargas úteis) cadastrados
@app.get("/osdr/payloads")
async def osdr_payloads():
    return await proxy(f"{OSDR}/geode-py/ws/api/payloads")

# Detalhes de um payload pelo identificador
@app.get("/osdr/payload/{identifier}")
async def osdr_payload(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/payload/{identifier}")

# Lista todos os hardwares cadastrados (equipamentos usados nas missões)
@app.get("/osdr/hardware")
async def osdr_hardware():
    return await proxy(f"{OSDR}/geode-py/ws/api/hardware")

# Detalhes de um hardware pelo identificador
@app.get("/osdr/hardware/{identifier}")
async def osdr_hardware_by_id(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/hardware/{identifier}")

# Lista todos os veículos espaciais cadastrados (ex: Dragon, Soyuz)
@app.get("/osdr/vehicles")
async def osdr_vehicles():
    return await proxy(f"{OSDR}/geode-py/ws/api/vehicles")

# Detalhes de um veículo pelo identificador
@app.get("/osdr/vehicle/{identifier}")
async def osdr_vehicle(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/vehicle/{identifier}")

# Lista todos os sujeitos de experimento (animais, plantas etc.)
@app.get("/osdr/subjects")
async def osdr_subjects():
    return await proxy(f"{OSDR}/geode-py/ws/api/subjects")

# Detalhes de um sujeito pelo identificador
@app.get("/osdr/subject/{identifier}")
async def osdr_subject(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/subject/{identifier}")

# Lista todos os bioespecimes (amostras biológicas coletadas nas missões)
@app.get("/osdr/biospecimens")
async def osdr_biospecimens():
    return await proxy(f"{OSDR}/geode-py/ws/api/biospecimens")

# Detalhes de um bioespecime pelo identificador
@app.get("/osdr/biospecimen/{identifier}")
async def osdr_biospecimen(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/biospecimen/{identifier}")
