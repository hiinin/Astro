import { ref, onMounted } from 'vue'

function buildUrl(path) {
  if (path.startsWith('http')) return path
  if (path.startsWith('/api')) return path
  return `/api${path.startsWith('/') ? path : `/${path}`}`
}

function resolveUrl(url) {
  return typeof url === 'function' ? url() : url
}

async function parseResponse(res, { parseErrorDetail = false } = {}) {
  if (!res.ok) {
    if (parseErrorDetail) {
      const body = await res.json().catch(() => null)
      throw new Error(body?.detail ?? String(res.status))
    }
    throw new Error(String(res.status))
  }
  return res.json()
}

export async function apiFetch(path, options = {}) {
  const res = await fetch(buildUrl(path))
  return parseResponse(res, options)
}

export function useApi(options = {}) {
  const {
    initialData = null,
    immediate = false,
    url,
    transform = (data) => data,
    parseErrorDetail = false,
  } = options

  const data = ref(initialData)
  const loading = ref(Boolean(immediate))
  const error = ref(null)
  const searched = ref(false)

  async function run(path, runOptions = {}) {
    const transformFn = runOptions.transform ?? transform
    const reset = runOptions.reset !== false

    loading.value = true
    error.value = null
    if (reset) data.value = initialData

    try {
      const json = await apiFetch(path, {
        parseErrorDetail: runOptions.parseErrorDetail ?? parseErrorDetail,
      })
      data.value = transformFn(json)
      return data.value
    } catch (e) {
      error.value = e.message
      if (reset) data.value = initialData
      return null
    } finally {
      loading.value = false
    }
  }

  async function search(path, searchOptions = {}) {
    searched.value = true
    return run(path, { ...searchOptions, reset: true })
  }

  if (immediate && url) {
    onMounted(() => run(resolveUrl(url)))
  }

  return { data, loading, error, searched, run, search }
}
