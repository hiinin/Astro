/**
 * Composable para o módulo EPIC (Earth Polychromatic Imaging Camera).
 */
import { ref } from 'vue'
import { apiFetch } from '../api/client.js'
import { useTabs } from '../api/useTabs.js'

const epicList = (json) => (Array.isArray(json) ? json : [])
const EPIC_DATE_TABS = new Set(['available', 'enh-available', 'natural-all', 'enhanced-all'])

export const EPIC_TABS = [
  { id: 'natural', label: 'Natural', path: '/epic/natural', mode: 'natural', transform: epicList },
  { id: 'natural-all', label: 'Natural · Todas', path: '/epic/natural/all', mode: 'natural', transform: epicList },
  { id: 'enhanced', label: 'Enhanced', path: '/epic/enhanced', mode: 'enhanced', transform: epicList },
  { id: 'enhanced-all', label: 'Enhanced · Todas', path: '/epic/enhanced/all', mode: 'enhanced', transform: epicList },
  { id: 'available', label: 'Datas · Natural', path: '/epic/natural/available', mode: 'natural', transform: epicList },
  { id: 'enh-available', label: 'Datas · Enhanced', path: '/epic/enhanced/available', mode: 'enhanced', transform: epicList },
]

export function epicImageUrl(img, mode = 'natural') {
  const [y, m, d] = img.date.split(' ')[0].split('-')
  return `https://epic.gsfc.nasa.gov/archive/${mode}/${y}/${m}/${d}/jpg/${img.image}.jpg`
}

export function epicDateOf(item) {
  return typeof item === 'string' ? item : item.date
}

export function useEpic() {
  const dateDetail = ref(null)
  const { tab, tabs, data, loading, error, load } = useTabs(EPIC_TABS)
  const mode = () => tabs.find((t) => t.id === tab.value)?.mode ?? 'natural'
  const isDates = () => EPIC_DATE_TABS.has(tab.value)
  const dateKind = () => (tab.value.startsWith('enh') ? 'enhanced' : 'natural')

  function switchTab(id) {
    dateDetail.value = null
    load(id)
  }

  async function loadDate(item) {
    dateDetail.value = await apiFetch(`/epic/${dateKind()}/date/${epicDateOf(item)}`)
  }

  return { tab, tabs, data, loading, error, dateDetail, mode, isDates, dateKind, switchTab, loadDate }
}
