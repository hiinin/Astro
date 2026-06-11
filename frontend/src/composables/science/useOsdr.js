/**
 * Composable para o módulo OSDR (Open Science Data Repository).
 */
import { ref, onMounted } from 'vue'
import { apiFetch } from '../api/client.js'
import { useRequest } from '../api/useRequest.js'

const SLUG = {
  missions: 'mission', experiments: 'experiment', payloads: 'payload',
  hardware: 'hardware', vehicles: 'vehicle', subjects: 'subject', biospecimens: 'biospecimen',
}
const URL_KEYS = Object.values(SLUG)

const LABELS = {
  identifier: 'Identificador', esID: 'ES ID', name: 'Nome', payloadName: 'Payload',
  section: 'Seção', type: 'Tipo', commonName: 'Nome comum', startDate: 'Início', endDate: 'Fim',
  protocol: 'Protocolo', category: 'Categoria', experimentalGroup: 'Grupo experimental',
}
const DETAIL_SKIP = new Set(['fields', 'hardware_version', 'parents', 'description', 'files', 'components', 'people', 'vehicle', 'biospecimens'])

function urlId(url) {
  const seg = typeof url === 'string' ? url.split('/').pop() : null
  return seg ? decodeURIComponent(seg) : null
}

export function itemKey(item) {
  for (const key of URL_KEYS) {
    const id = urlId(item?.[key])
    if (id) return id
  }
  return item?.identifier ?? item?.id ?? item?.name ?? item?.Name
}

export function osdPagePath(section, item) {
  const slug = SLUG[section]
  const id = itemKey(item)
  return slug && id ? `/ciencia-aberta/${slug}/${encodeURIComponent(id)}` : null
}

export const OSDR_TYPE_LABELS = {
  mission: 'Missão', experiment: 'Experimento', payload: 'Payload', hardware: 'Hardware',
  vehicle: 'Veículo', subject: 'Sujeito', biospecimen: 'Biospecimen',
}

export const OSDR_TABS = [
  { id: 'missions', label: 'Missões', path: '/osdr/missions' },
  { id: 'experiments', label: 'Experimentos', path: '/osdr/experiments' },
  { id: 'payloads', label: 'Payloads', path: '/osdr/payloads' },
  { id: 'hardware', label: 'Hardware', path: '/osdr/hardware' },
  { id: 'vehicles', label: 'Veículos', path: '/osdr/vehicles' },
  { id: 'subjects', label: 'Sujeitos', path: '/osdr/subjects' },
  { id: 'biospecimens', label: 'Biospecimens', path: '/osdr/biospecimens' },
]

export function osdDetailTitle(d) {
  if (!d) return '—'
  return d.name ?? d.payloadName ?? d.fields?.[0]?.title
    ?? d.commonName?.annotationValue ?? d.type?.annotationValue ?? d.identifier ?? '—'
}

export function osdLinkedItem(link) {
  if (!link || typeof link !== 'object') return null
  for (const key of URL_KEYS) {
    const id = urlId(link[key])
    if (id) return { type: key, id }
  }
  return null
}

export function osdParentLinks(parents) {
  if (!parents || typeof parents !== 'object') return []
  return Object.entries(parents).flatMap(([type, list]) =>
    (list ?? []).flatMap((entry) => {
      const id = urlId(entry?.[type])
      return id ? [{ type, id }] : []
    }),
  )
}

function formatVal(v) {
  if (v == null || v === '') return null
  if (typeof v === 'object' && 'annotationValue' in v) return v.annotationValue || null
  if (typeof v === 'string' || typeof v === 'number' || typeof v === 'boolean') return String(v)
  const link = osdLinkedItem(v)
  if (link) return { link }
  if (Array.isArray(v)) {
    if (!v.length) return null
    if (v.every((x) => typeof x === 'string')) return v.join(', ')
    const links = v.map(osdLinkedItem).filter(Boolean)
    if (links.length === v.length) return { links }
    const parts = v.map(formatVal).filter((x) => typeof x === 'string')
    return parts.length ? parts.join(', ') : null
  }
  if (typeof v === 'object') {
    if (v.versionName) return v.versionName + (v.version != null ? ` (v${v.version})` : '')
    const parts = Object.entries(v)
      .filter(([k, val]) => val != null && val !== '' && !['id', 'mapping', 'branch', 'definition', 'termSource', 'termAccession', 'freeOntology'].includes(k) && !k.endsWith('Lowercase'))
      .map(([k, val]) => { const s = formatVal(val); return typeof s === 'string' ? `${k}: ${s}` : null })
      .filter(Boolean)
    return parts.length ? parts.join(' · ') : null
  }
  return String(v)
}

export function osdRows(obj, skip = new Set()) {
  if (!obj || typeof obj !== 'object') return []
  return Object.entries(obj)
    .filter(([k, v]) => !skip.has(k) && v != null && v !== '' && k !== 'id')
    .flatMap(([key, value]) => {
      const formatted = formatVal(value)
      if (formatted == null) return []
      const row = { label: LABELS[key] ?? key, key }
      if (typeof formatted === 'object' && formatted.link) return [{ ...row, link: formatted.link }]
      if (typeof formatted === 'object' && formatted.links) return [{ ...row, links: formatted.links }]
      return [{ ...row, value: formatted }]
    })
}

export function osdDetailRows(item) {
  return osdRows(item, DETAIL_SKIP)
}

function normalizeStudy(hit) {
  const src = hit._source ?? hit
  const mission = src.Mission
  const missionName = mission?.Name?.trim()
  const year = mission?.['Start Date']?.match(/\d{4}/)?.[0]
  return {
    id: src['Study Identifier'] ?? hit._id,
    title: src['Project Title']?.trim() || src['Study Title']?.trim() || 'Sem título',
    mission: missionName ? (year ? `${missionName} (${year})` : missionName) : null,
    program: src['Flight Program']?.trim() || null,
    area: src['Study Assay Measurement Type']?.trim() || src['Material Type']?.trim() || null,
    description: src['Study Description']?.trim() || src['Study Protocol Description']?.trim() || null,
    raw: src,
  }
}

export function useOsdr() {
  const query = ref('')
  const section = ref('search')
  const studies = ref([])
  const total = ref(0)
  const selected = ref(null)
  const showRaw = ref(false)
  const meta = ref(null)
  const files = ref(null)
  const osdData = ref(null)
  const { loading, error, run } = useRequest()
  const { loading: osdLoading, error: osdError, run: osdRun } = useRequest()

  async function loadStudies() {
    const q = query.value.trim()
    const json = await run(q ? `/osdr/search?q=${encodeURIComponent(q)}` : '/osdr/search')
    if (!json) { studies.value = []; total.value = 0; return }
    total.value = json.hits?.total ?? 0
    studies.value = (json.hits?.hits ?? [])
      .map(normalizeStudy)
      .filter((s) => s.mission || s.program || (s.description && s.title.length > 20))
  }

  async function selectStudy(study) {
    selected.value = study
    showRaw.value = false
    meta.value = null
    files.value = null
    try {
      const [m, f] = await Promise.all([
        apiFetch(`/osdr/study/meta/${study.id}`),
        apiFetch(`/osdr/study/files/${study.id}`),
      ])
      meta.value = m
      files.value = f
    } catch {}
  }

  async function pickSection(id) {
    section.value = id
    osdData.value = null
    if (id === 'search') return
    const tab = OSDR_TABS.find((t) => t.id === id)
    osdData.value = await osdRun(tab.path, {
      transform: (json) => Array.isArray(json) ? json : (json?.data ?? json?.items ?? []),
    })
  }

  onMounted(loadStudies)

  return {
    query, section, studies, total, selected, showRaw, meta, files, osdData,
    loading, error, osdLoading, osdError, loadStudies, selectStudy, pickSection,
  }
}
