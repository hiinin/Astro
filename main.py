from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(
    title="NASA API Proxy",
    version="1.0.0",
)

API_KEY = "DEMO_KEY"  # Substitua em api.nasa.gov

NASA    = "https://api.nasa.gov"
IMAGES  = "https://images-api.nasa.gov"
SSD     = "https://ssd-api.jpl.nasa.gov"
EONET   = "https://eonet.gsfc.nasa.gov/api/v3"
TLE     = "https://tle.ivanstanojevic.me/api/tle"
EXO     = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"
OSDR    = "https://osdr.nasa.gov"


async def proxy(url: str, params: dict = {}) -> JSONResponse:
    async with httpx.AsyncClient() as c:
        r = await c.get(url, params=params)
        return r.json()


# ── APOD ──────────────────────────────────────────────────────────────────────

# Retorna a imagem astronômica do dia com título, descrição e URL
# Parâmetros: date (YYYY-MM-DD), start_date, end_date, count, thumbs, hd
@app.get("/apod")
async def apod(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/apod", params)


# ── NeoWs - Asteroides Próximos da Terra ──────────────────────────────────────

# Lista asteroides que se aproximaram da Terra em um intervalo de datas
# Parâmetros: start_date (YYYY-MM-DD), end_date (máximo 7 dias após start_date)
@app.get("/neo/feed")
async def neo_feed(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/neo/rest/v1/feed", params)

# Navega pelo dataset completo de asteroides (retorna paginado)
@app.get("/neo/browse")
async def neo_browse():
    return await proxy(f"{NASA}/neo/rest/v1/neo/browse", {"api_key": API_KEY})

# Busca um asteroide específico pelo ID SPK do NASA JPL
@app.get("/neo/lookup/{asteroid_id}")
async def neo_lookup(asteroid_id: int):
    return await proxy(f"{NASA}/neo/rest/v1/neo/{asteroid_id}", {"api_key": API_KEY})


# ── DONKI - Banco de Dados de Clima Espacial ──────────────────────────────────
# Todos os endpoints aceitam: startDate e endDate (YYYY-MM-DD)

# Ejeção de Massa Coronal: nuvens de plasma lançadas pelo Sol em direção à Terra
@app.get("/donki/cme")
async def donki_cme(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/CME", params)

# Análise técnica das ejeções de massa coronal
# Parâmetros extras: mostAccurateOnly, speed, halfAngle, catalog (ALL | SWRC_CATALOG | JANG_ET_AL_CATALOG)
@app.get("/donki/cme-analysis")
async def donki_cme_analysis(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/CMEAnalysis", params)

# Tempestade geomagnética: perturbações no campo magnético da Terra causadas pelo Sol
@app.get("/donki/gst")
async def donki_gst(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/GST", params)

# Choque interplanetário: ondas de choque no vento solar
# Parâmetros extras: location (ALL | Earth | MESSENGER | STEREO A | STEREO B), catalog
@app.get("/donki/ips")
async def donki_ips(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/IPS", params)

# Explosão solar: liberação intensa de energia eletromagnética na superfície do Sol
@app.get("/donki/flr")
async def donki_flr(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/FLR", params)

# Partícula solar energética: partículas de alta energia emitidas pelo Sol
@app.get("/donki/sep")
async def donki_sep(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/SEP", params)

# Cruzamento da magnetopausa: quando o vento solar empurra a magnetosfera para dentro
@app.get("/donki/mpc")
async def donki_mpc(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/MPC", params)

# Aumento do cinturão de radiação: intensificação da radiação nos cinturões de Van Allen
@app.get("/donki/rbe")
async def donki_rbe(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/RBE", params)

# Corrente de alta velocidade: fluxo rápido de vento solar vindo de buracos coronais
@app.get("/donki/hss")
async def donki_hss(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/HSS", params)

# Simulação WSA+Enlil: modelo computacional de propagação do vento solar
@app.get("/donki/wsa-enlil")
async def donki_wsa_enlil(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/WSAEnlilSimulations", params)

# Notificações oficiais de eventos de clima espacial
# Parâmetro extra: type (all | FLR | SEP | CME | IPS | MPC | GST | RBE | report)
@app.get("/donki/notifications")
async def donki_notifications(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/DONKI/notifications", params)


# ── EPIC - Câmera de Imagem Policromática da Terra (satélite DSCOVR) ──────────

# Metadados da imagem natural mais recente da Terra (cor real)
@app.get("/epic/natural")
async def epic_natural():
    return await proxy(f"{NASA}/EPIC/api/natural", {"api_key": API_KEY})

# Lista de todas as datas com imagens naturais disponíveis
@app.get("/epic/natural/all")
async def epic_natural_all():
    return await proxy(f"{NASA}/EPIC/api/natural/all", {"api_key": API_KEY})

# Lista de datas com imagens naturais disponíveis (formato alternativo)
@app.get("/epic/natural/available")
async def epic_natural_available():
    return await proxy(f"{NASA}/EPIC/api/natural/available", {"api_key": API_KEY})

# Imagens naturais da Terra de uma data específica (YYYY-MM-DD)
@app.get("/epic/natural/date/{date}")
async def epic_natural_date(date: str):
    return await proxy(f"{NASA}/EPIC/api/natural/date/{date}", {"api_key": API_KEY})

# Metadados da imagem aprimorada mais recente (cores intensificadas para análise científica)
@app.get("/epic/enhanced")
async def epic_enhanced():
    return await proxy(f"{NASA}/EPIC/api/enhanced", {"api_key": API_KEY})

# Lista de todas as datas com imagens aprimoradas disponíveis
@app.get("/epic/enhanced/all")
async def epic_enhanced_all():
    return await proxy(f"{NASA}/EPIC/api/enhanced/all", {"api_key": API_KEY})

# Lista de datas com imagens aprimoradas disponíveis (formato alternativo)
@app.get("/epic/enhanced/available")
async def epic_enhanced_available():
    return await proxy(f"{NASA}/EPIC/api/enhanced/available", {"api_key": API_KEY})

# Imagens aprimoradas da Terra de uma data específica (YYYY-MM-DD)
@app.get("/epic/enhanced/date/{date}")
async def epic_enhanced_date(date: str):
    return await proxy(f"{NASA}/EPIC/api/enhanced/date/{date}", {"api_key": API_KEY})


# ── InSight - Clima em Marte ───────────────────────────────────────────────────

# Dados meteorológicos dos últimos 7 Sols (dias marcianos): temperatura, vento e pressão
# Coletados pelo lander InSight na planície de Elysium Planitia em Marte
@app.get("/insight/weather")
async def insight_weather(request: Request):
    params = {"api_key": API_KEY, "feedtype": "json", "ver": "1.0", **request.query_params}
    return await proxy(f"{NASA}/insight_weather/", params)


# ── Mars Rovers - Fotos dos Rovers em Marte ───────────────────────────────────

# Fotos tiradas por um rover em Marte
# rover: curiosity | opportunity | spirit | perseverance
# Parâmetros: sol (dia marciano), earth_date (YYYY-MM-DD), camera, page
@app.get("/mars-rovers/{rover}/photos")
async def mars_rover_photos(rover: str, request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/mars-photos/api/v1/rovers/{rover}/photos", params)

# Manifesto da missão do rover: status, datas de operação, total de fotos e câmeras disponíveis
@app.get("/mars-rovers/{rover}/manifesto")
async def mars_rover_manifesto(rover: str):
    return await proxy(f"{NASA}/mars-photos/api/v1/manifests/{rover}", {"api_key": API_KEY})


# ── NASA Image & Video Library - Acervo de Mídia da NASA ──────────────────────

# Busca imagens, vídeos e áudios no acervo da NASA
# Parâmetros: q (termo de busca), media_type (image | video | audio), year_start, year_end, page
@app.get("/images/search")
async def images_search(request: Request):
    return await proxy(f"{IMAGES}/search", dict(request.query_params))

# Manifesto de um ativo de mídia: lista com todas as URLs dos arquivos disponíveis
@app.get("/images/asset/{nasa_id}")
async def images_asset(nasa_id: str):
    return await proxy(f"{IMAGES}/asset/{nasa_id}")

# URL do arquivo de metadados (JSON) de um ativo de mídia
@app.get("/images/metadata/{nasa_id}")
async def images_metadata(nasa_id: str):
    return await proxy(f"{IMAGES}/metadata/{nasa_id}")

# URL do arquivo de legendas (.SRT) de um vídeo
@app.get("/images/captions/{nasa_id}")
async def images_captions(nasa_id: str):
    return await proxy(f"{IMAGES}/captions/{nasa_id}")

# Conteúdo de um álbum de mídia pelo nome
@app.get("/images/album/{album_name}")
async def images_album(album_name: str):
    return await proxy(f"{IMAGES}/album/{album_name}")


# ── TechTransfer - Patentes, Software e Spinoffs da NASA ──────────────────────

# Busca patentes da NASA por termo (ex: ?patent=engine)
@app.get("/techtransfer/patent")
async def techtransfer_patent(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/patent/", params)

# Busca informações sobre patentes já emitidas (ex: ?patent_issued=propulsion)
@app.get("/techtransfer/patent-issued")
async def techtransfer_patent_issued(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/patent_issued/", params)

# Busca software open-source desenvolvido pela NASA (ex: ?software=satellite)
@app.get("/techtransfer/software")
async def techtransfer_software(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/software/", params)

# Busca exemplos de tecnologia NASA transferida ao setor privado (ex: ?spinoff=medical)
@app.get("/techtransfer/spinoff")
async def techtransfer_spinoff(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/techtransfer/spinoff/", params)


# ── SSD/CNEOS - Dinâmica do Sistema Solar e Objetos Próximos da Terra ─────────

# Dados de aproximação de asteroides e cometas aos planetas
# Parâmetros: date-min, date-max, dist-max (em AU, ex: 0.05), neo (true/false)
@app.get("/ssd/cad")
async def ssd_cad(request: Request):
    return await proxy(f"{SSD}/cad.api", dict(request.query_params))

# Bolas de fogo (meteoros brilhantes) detectadas por sensores do governo americano
# Parâmetros: date-min, date-max, energy-min (em kt), req-loc (true/false)
@app.get("/ssd/fireball")
async def ssd_fireball(request: Request):
    return await proxy(f"{SSD}/fireball.api", dict(request.query_params))

# NEOs acessíveis para futuras missões tripuladas (NHATS)
# Parâmetros: dv (delta-v em km/s), dur (duração da missão em dias), stay, launch (ex: 2025-2030)
@app.get("/ssd/nhats")
async def ssd_nhats(request: Request):
    return await proxy(f"{SSD}/nhats.api", dict(request.query_params))

# Dados em tempo real do Scout: risco de impacto de objetos recém-descobertos
# Parâmetro: tdes (designação temporária do objeto, ex: P21dS9Y)
@app.get("/ssd/scout")
async def ssd_scout(request: Request):
    return await proxy(f"{SSD}/scout.api", dict(request.query_params))

# Avaliação de risco de impacto de NEOs na Terra pelo sistema Sentry
# Parâmetros: spk (ID numérico do objeto), des (designação), removed (objetos retirados da lista)
@app.get("/ssd/sentry")
async def ssd_sentry(request: Request):
    return await proxy(f"{SSD}/sentry.api", dict(request.query_params))


# ── EONET - Rastreador de Eventos Naturais da Terra ───────────────────────────

# Lista eventos naturais monitorados pela NASA (furacões, incêndios, vulcões, etc.)
# Parâmetros: status (open | closed), limit, days, source, category, bbox
@app.get("/eonet/events")
async def eonet_events(request: Request):
    return await proxy(f"{EONET}/events", dict(request.query_params))

# Detalhes completos de um evento natural específico pelo seu ID
@app.get("/eonet/events/{event_id}")
async def eonet_event_by_id(event_id: str):
    return await proxy(f"{EONET}/events/{event_id}")

# Lista todas as categorias de eventos disponíveis (wildfires, volcanoes, storms, etc.)
@app.get("/eonet/categories")
async def eonet_categories():
    return await proxy(f"{EONET}/categories")

# Lista eventos filtrados por uma categoria específica
# Parâmetros: status, limit, days
@app.get("/eonet/categories/{category_id}")
async def eonet_events_by_category(category_id: str, request: Request):
    return await proxy(f"{EONET}/categories/{category_id}", dict(request.query_params))

# Lista todas as camadas de imagens de satélite vinculadas a eventos naturais
@app.get("/eonet/layers")
async def eonet_layers():
    return await proxy(f"{EONET}/layers")

# Lista camadas de imagens de satélite filtradas por categoria de evento
@app.get("/eonet/layers/{category_id}")
async def eonet_layers_by_category(category_id: str):
    return await proxy(f"{EONET}/layers/{category_id}")


# ── TLE API - Elementos Orbitais de Satélites ─────────────────────────────────

# Busca satélites pelo nome (ex: ?search=ISS)
# Retorna o TLE: dois conjuntos de dados que descrevem a órbita de um satélite
@app.get("/tle")
async def tle_search(request: Request):
    return await proxy(TLE, dict(request.query_params))

# Retorna o TLE de um satélite específico pelo número NORAD (ex: 25544 = ISS)
@app.get("/tle/{satellite_id}")
async def tle_by_id(satellite_id: int):
    return await proxy(f"{TLE}/{satellite_id}")


# ── Exoplanet Archive - Arquivo de Exoplanetas da NASA ────────────────────────

# Consulta o banco de dados de exoplanetas confirmados e candidatos
# Parâmetros: table (exoplanets | cumulative), select (colunas), where (filtro SQL ex: pl_tranflag=1)
@app.get("/exoplanet")
async def exoplanet(request: Request):
    params = {"format": "json", **request.query_params}
    return await proxy(EXO, params)


# ── OSDR - Repositório de Ciência Aberta da NASA ──────────────────────────────

# Lista os arquivos de dados de um estudo OSD (ex: /osdr/study/files/87)
# Parâmetros: page, size
@app.get("/osdr/study/files/{study_ids}")
async def osdr_study_files(study_ids: str, request: Request):
    return await proxy(f"{OSDR}/osdr/data/osd/files/{study_ids}", dict(request.query_params))

# Retorna os metadados completos de um estudo OSD pelo número (ex: 87)
@app.get("/osdr/study/meta/{study_id}")
async def osdr_study_meta(study_id: int):
    return await proxy(f"{OSDR}/osdr/data/osd/meta/{study_id}")

# Busca datasets por palavra-chave no repositório de ciência aberta
# Parâmetros: term, from, size, type (cgene | nih_geo_gse | ebi_pride | mg_rast)
@app.get("/osdr/search")
async def osdr_search(request: Request):
    return await proxy(f"{OSDR}/osdr/data/search", dict(request.query_params))

# Lista todos os experimentos científicos cadastrados no OSDR
@app.get("/osdr/experiments")
async def osdr_experiments():
    return await proxy(f"{OSDR}/geode-py/ws/api/experiments")

# Retorna os detalhes de um experimento específico pelo identificador
@app.get("/osdr/experiment/{identifier}")
async def osdr_experiment(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/experiment/{identifier}")

# Lista todas as missões espaciais cadastradas no OSDR
@app.get("/osdr/missions")
async def osdr_missions():
    return await proxy(f"{OSDR}/geode-py/ws/api/missions")

# Retorna os detalhes de uma missão específica pelo identificador (ex: SpaceX-12)
@app.get("/osdr/mission/{identifier}")
async def osdr_mission(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/mission/{identifier}")

# Lista todos os payloads (cargas úteis) das missões cadastradas
@app.get("/osdr/payloads")
async def osdr_payloads():
    return await proxy(f"{OSDR}/geode-py/ws/api/payloads")

# Retorna os detalhes de um payload específico pelo identificador
@app.get("/osdr/payload/{identifier}")
async def osdr_payload(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/payload/{identifier}")

# Lista todos os hardwares (equipamentos) utilizados nas missões
@app.get("/osdr/hardware")
async def osdr_hardware():
    return await proxy(f"{OSDR}/geode-py/ws/api/hardware")

# Retorna os detalhes de um hardware específico pelo identificador
@app.get("/osdr/hardware/{identifier}")
async def osdr_hardware_by_id(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/hardware/{identifier}")

# Lista todos os veículos espaciais cadastrados (ex: Dragon, Soyuz)
@app.get("/osdr/vehicles")
async def osdr_vehicles():
    return await proxy(f"{OSDR}/geode-py/ws/api/vehicles")

# Retorna os detalhes de um veículo espacial específico pelo identificador
@app.get("/osdr/vehicle/{identifier}")
async def osdr_vehicle(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/vehicle/{identifier}")

# Lista todos os sujeitos de experimento cadastrados (animais, plantas, etc.)
@app.get("/osdr/subjects")
async def osdr_subjects():
    return await proxy(f"{OSDR}/geode-py/ws/api/subjects")

# Retorna os detalhes de um sujeito de experimento específico pelo identificador
@app.get("/osdr/subject/{identifier}")
async def osdr_subject(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/subject/{identifier}")

# Lista todos os bioespecimes (amostras biológicas coletadas nas missões)
@app.get("/osdr/biospecimens")
async def osdr_biospecimens():
    return await proxy(f"{OSDR}/geode-py/ws/api/biospecimens")

# Retorna os detalhes de um bioespecime específico pelo identificador
@app.get("/osdr/biospecimen/{identifier}")
async def osdr_biospecimen(identifier: str):
    return await proxy(f"{OSDR}/geode-py/ws/api/biospecimen/{identifier}")

# ── Earth - Imagens Landsat 8 de pontos geográficos ──────────────────────────

# Retorna a imagem de satélite Landsat 8 de uma coordenada geográfica
# Parâmetros obrigatórios: lat, lon | Opcionais: date (YYYY-MM-DD), dim (graus, padrão 0.025)
@app.get("/earth/imagery")
async def earth_imagery(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/earth/imagery", params)

# Retorna os metadados e URL da imagem Landsat mais próxima de uma data e coordenada
# Parâmetros obrigatórios: lat, lon | Opcionais: date (YYYY-MM-DD), dim
@app.get("/earth/assets")
async def earth_assets(request: Request):
    params = {"api_key": API_KEY, **request.query_params}
    return await proxy(f"{NASA}/planetary/earth/assets", params)


# ── Techport - Portfólio de Tecnologia da NASA ────────────────────────────────

TECHPORT = "https://techport.nasa.gov/api"

# Lista todos os projetos de tecnologia ativos e concluídos da NASA
@app.get("/techport/projects")
async def techport_projects(request: Request):
    return await proxy(f"{TECHPORT}/projects", dict(request.query_params))

# Retorna os detalhes completos de um projeto de tecnologia pelo ID
@app.get("/techport/projects/{project_id}")
async def techport_project(project_id: int):
    return await proxy(f"{TECHPORT}/projects/{project_id}")
