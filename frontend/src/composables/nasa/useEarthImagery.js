/**
 * Composable para imagens de satélite da Terra (Landsat/Sentinel).
 */
import { ref, onMounted } from 'vue'
import { apiFetch } from '../api/client.js'
import { useRequest } from '../api/useRequest.js'

function qs(params) {
  return new URLSearchParams(
    Object.entries(params).filter(([, v]) => v != null && v !== ''),
  ).toString()
}

function pickDateRange(dates, current = '') {
  if (!dates?.length) return { min: '', max: '', date: current }
  const max = dates[0]
  const min = dates[dates.length - 1]
  const date = !current || current < min || current > max ? max : current
  return { min, max, date }
}

export function useEarthImagery() {
  const lat = ref('-23.5')
  const lon = ref('-46.6')
  const dim = ref('1')
  const date = ref('')
  const minDate = ref('')
  const maxDate = ref('')
  const { data: result, loading, error, searched, search } = useRequest()

  async function handleSearch() {
    const { dates } = await apiFetch(`/earth/assets?${qs({ lat: lat.value, lon: lon.value })}`)
    const range = pickDateRange(dates, date.value)
    minDate.value = range.min
    maxDate.value = range.max
    date.value = range.date
    await search(`/earth/imagery?${qs({ lat: lat.value, lon: lon.value, dim: dim.value, date: date.value })}`)
  }

  onMounted(handleSearch)

  return { lat, lon, dim, date, minDate, maxDate, result, loading, error, searched, handleSearch }
}
