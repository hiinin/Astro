# Documentação de Migração — Astro ← Lunar-Engine

**Data:** 11 de Junho de 2026  
**Foco:** Camada de dados e integração com API (NÃO altera visual/layout/CSS)

---

## PARTE 1 — O que o ASTRO tem que o Lunar-Engine NÃO tem

Estas funcionalidades são **exclusivas do Astro** e serão **preservadas integralmente**:

| Item | Arquivo | Descrição |
|------|---------|-----------|
| Rota `/inicio` | `modules/inicio/inicioView.vue` | Página "Explorar" com grid de navegação para todas as seções |
| Endpoint `/neo/stats` | `routers/asteroides.py` | Retorna estatísticas gerais dos NEOs |
| DashboardView com imagem hero | `modules/DashboardView.vue` | Layout split com imagem `nasa-space.jpg` (Lunar usa só texto) |
| ExoplanetasView avançada | `modules/exoplanetas/ExoplanetasView.vue` | View com stats, visualização de planeta, grid/list view, filtros por método (Lunar tem apenas tabela simples) |
| AsteroidesView com cards visuais | `modules/asteroides/AsteroidesView.vue` | Cards com badges, cores, grid responsivo (Lunar usa tabela simples) |
| AsteroidesDetailView rica | `modules/asteroides/AsteroidesDetailView.vue` | Tabela detalhada com classe orbital inline (Lunar usa cards separados) |
| ProjetosView com cards e detalhes inline | `modules/projetos/ProjetosView.vue` | Cards com status, descrição, animações (Lunar usa tabela simples) |
| ProjetosDetalhe completo | `modules/projetos/ProjetosDetalhe.vue` | Hero section, timeline, áreas tecnológicas, sidebar (Lunar é mais simples) |
| EventosNaturaisView com cards coloridos | `modules/eventosnaturais/EventosNaturaisView.vue` | Cards com gradientes por categoria (Lunar usa tabela) |
| RoversMarteDetalhe com fotos grandes | `modules/roversmarte/RoversMarteDetalhe.vue` | Cards horizontais com imagem 224px (Lunar usa grid quadrado) |
| SatelitesView com cards grid | `modules/satelites/SatelitesView.vue` | Cards 4 colunas com dados orbitais (Lunar usa tabela) |
| CienciaAbertaView split-layout | `modules/cienciaaberta/CienciaAbertaView.vue` | Layout dividido cards+detalhe lateral (Lunar usa tabs+tabela) |
| Astro useApi com `parseErrorDetail` | `composables/useApi.js` | Opção para extrair `detail` do body de erro (Lunar não tem) |
| TechTransferView com selector visual | `modules/techtransfer/TechTransferView.vue` | Botões de categoria com animações e cores (Lunar não tem essa view avançada) |
| ClimaMarteView tabela detalhada | `modules/climamarte/ClimaMarteView.vue` | Tabela com média/min/max/obs e footer com sol/season |

**Conclusão:** O Astro tem design e visual MUITO mais elaborado. Tudo será preservado.

---

## PARTE 2 — O que o Lunar-Engine tem que o Astro NÃO tem (foco: dados)

### 2.1 Composables AUSENTES no Astro

| # | Composable | Funções | Impacto |
|---|-----------|---------|---------|
| 1 | `donki.js` | `DONKI_TABS`, `donkiStart()`, `donkiId()`, `donkiNote()` | ClimaEspacialView usa apenas 4 de 10 tabs |
| 2 | `useEpic.js` | `EPIC_TABS`, `epicImageUrl()`, `epicDateOf()`, `useEpic()` | CameraTeraView carrega apenas natural estático |
| 3 | `useMedia.js` | `mediaThumb()`, `mediaAssetUrl()`, `mediaVideoUrl()`, `mediaIsVideo()`, `mediaAssetFiles()`, `mediaParseError()`, `useMedia()` | MidiasView não tem detalhe/álbum/vídeo |
| 4 | `useOsdr.js` | `OSDR_TABS`, `itemKey()`, `osdPagePath()`, `osdDetailTitle()`, `useOsdr()` e mais | CienciaAbertaView não navega pelas 7 seções OSDR |
| 5 | `useEarthImagery.js` | `useEarthImagery()` com busca de datas disponíveis | ImagensTerraView não busca datas disponíveis antes |

### 2.2 Funções AUSENTES no `useApi.js` do Astro

| # | Função | Descrição |
|---|--------|-----------|
| 6 | `useTabs(tabs)` | Helper para navegação de tabs com carregamento automático |
| 7 | `tabClass(active)` | Classes CSS para tabs ativas/inativas |
| 8 | `useFetchDetail()` | Ref reativa para carregar detalhe de um item selecionado |

### 2.3 Views AUSENTES no Astro

| # | View | Rota | Descrição |
|---|------|------|-----------|
| 9 | `MidiasDetalhe.vue` | `/midias/:id` | Detalhe de uma mídia (asset, vídeo, imagem grande) |
| 10 | `MidiasAlbumView.vue` | `/midias/album/:id` | Navegação de álbum NASA |
| 11 | `SatelitesDetalhe.vue` | `/satelites/:id` | Detalhe orbital de satélite específico |
| 12 | `CienciaAbertaDetalhe.vue` | `/ciencia-aberta/:type/:id` | Detalhe de entidade OSDR (missão, experimento, etc.) |

### 2.4 Integrações de DADOS faltando nas views existentes

| # | View | O que falta (dados, NÃO visual) |
|---|------|----------------------------------|
| 13 | ClimaEspacialView | Faltam 6 tabs: `cme-analysis`, `ips`, `sep`, `rbe`, `hss`, `wsa-enlil` |
| 14 | CameraTeraView | Faltam tabs: enhanced, all, available, navegação por data |
| 15 | ImagensTerraView | Falta buscar `/earth/assets` para datas disponíveis + seletor de data |
| 16 | MidiasView | Falta: navegar para detalhe, abrir álbum |
| 17 | CienciaAbertaView | Faltam 7 seções OSDR: missions, experiments, payloads, hardware, vehicles, subjects, biospecimens |
| 18 | SistemaSolarView | Faltam 2 tabs: nhats, scout (com transform adequado) |
| 19 | EventosNaturaisView | Faltam tabs: categorias, camadas (usa endpoint `/eonet/categories` e `/eonet/layers`) |
| 20 | SatelitesView | Falta: clicar em satélite navega para detalhe (`/satelites/:id`) |
| 21 | RoversMarteDetalhe | Falta: tab manifesto com seletor de data e busca por `earth_date` |
| 22 | AsteroidesView | Falta: tab "Feed" (`/neo/feed`) além do browse |

### 2.5 Componentes UI ausentes no Astro

| # | Componente | Descrição |
|---|-----------|-----------|
| 23 | `components/ui/LazyImg.vue` | Imagem com lazy loading via IntersectionObserver |
| 24 | `components/ui/NasaLoader.vue` | Loader animado com foguete (NÃO é obrigatório — Astro já tem seu loader inline) |

---

## PARTE 3 — PLANO DE MIGRAÇÃO PARCIAL (por fases seguras)

### FASE 1 — Funções base no useApi.js (BAIXO RISCO)
**Arquivo:** `frontend/src/composables/useApi.js`  
**Ação:** Adicionar `useTabs()`, `tabClass()`, `useFetchDetail()` ao final do arquivo  
**Risco:** ZERO — são adições puras, não alteram nada existente  
**Teste:** Todas as views existentes continuam funcionando normalmente

### FASE 2 — Composables novos (ZERO RISCO)
**Arquivos novos:**
- `frontend/src/composables/donki.js`
- `frontend/src/composables/useEpic.js`
- `frontend/src/composables/useMedia.js`
- `frontend/src/composables/useOsdr.js`
- `frontend/src/composables/useEarthImagery.js`

**Risco:** ZERO — são arquivos novos que não afetam nada existente

### FASE 3 — Views novas + rotas (BAIXO RISCO)
**Arquivos novos:**
- `frontend/src/modules/midias/MidiasDetalhe.vue`
- `frontend/src/modules/midias/MidiasAlbumView.vue`
- `frontend/src/modules/satelites/SatelitesDetalhe.vue`
- `frontend/src/modules/cienciaaberta/CienciaAbertaDetalhe.vue`

**Arquivo modificado:** `frontend/src/router/index.js` (adicionar 4 rotas)  
**Risco:** BAIXO — adiciona rotas, não remove nenhuma

### FASE 4 — Atualização da camada de dados nas views (MÉDIO RISCO)
Cada view será atualizada individualmente, **preservando 100% do template/CSS**:

| Ordem | View | Alteração |
|-------|------|-----------|
| 4.1 | ClimaEspacialView | Expandir tabs de 4 para 10 (apenas `<script>` + lista de tabs no template) |
| 4.2 | SistemaSolarView | Adicionar 2 tabs (nhats, scout) com transforms |
| 4.3 | CameraTeraView | Adicionar tabs enhanced/available/date ao `<script>` |
| 4.4 | ImagensTerraView | Integrar busca de datas disponíveis no `<script>` |
| 4.5 | EventosNaturaisView | Adicionar tabs categorias/camadas no `<script>` |
| 4.6 | MidiasView | Adicionar navegação para detalhe/álbum |
| 4.7 | CienciaAbertaView | Adicionar navegação por seções OSDR |
| 4.8 | SatelitesView | Adicionar click para navegar ao detalhe |
| 4.9 | RoversMarteDetalhe | Adicionar tab manifesto com date picker |
| 4.10 | AsteroidesView | Adicionar tab Feed |

---

## PARTE 4 — REGRAS DE IMPLEMENTAÇÃO

1. **NÃO alterar** CSS, classes Tailwind, layout, templates visuais
2. **NÃO alterar** componentes em `components/layout/` ou `components/home/`
3. **NÃO refatorar** código existente que funciona
4. **NÃO remover** funcionalidades que o Astro tem a mais
5. **PRESERVAR** o estilo visual do Astro (cards, grids, cores, animações)
6. Cada fase deve ser testável independentemente
7. Se uma fase quebrar algo, reverter e tentar abordagem diferente

---

## PARTE 5 — RESUMO DE AÇÕES

| Fase | Arquivos criados | Arquivos modificados | Risco |
|------|-----------------|---------------------|-------|
| 1 | 0 | 1 (useApi.js) | Zero |
| 2 | 5 | 0 | Zero |
| 3 | 4 | 1 (router) | Baixo |
| 4 | 0 | 10 | Médio (parcial) |
| **Total** | **9** | **12** | — |

---

**⚠️ AGUARDANDO APROVAÇÃO ANTES DE INICIAR QUALQUER IMPLEMENTAÇÃO.**

Qual fase quer que eu comece? Posso ir uma por uma para você validar cada passo.
