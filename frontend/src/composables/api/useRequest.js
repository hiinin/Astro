/**
 * Composable genérico para requisições reativas.
 * Antigo "useApi" — renomeado para deixar claro que é um wrapper de request.
 */
import { ref, onMounted } from 'vue'
import { apiFetch } from './client.js'

function resolveUrl(url) {
  return typeof url === 'function' ? url() : url
}

/**
 * @param {object} options
 * @param {*}        options.initialData   - valor inicial do ref `data`
 * @param {boolean}  options.immediate     - dispara na montagem
 * @param {string|Function} options.url    - URL (ou factory) para immediate
 * @param {Function} options.transform     - transforma o JSON antes de guardar
 * @param {boolean}  options.parseErrorDetail - extrai `detail` do body de erro
 */
export function useRequest(options = {}) {
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

/**
 * Composable minimalista para carregar um detalhe avulso.
 */
export function useFetchDetail() {
  const detail = ref(null)
  async function load(path) {
    if (path) detail.value = await apiFetch(path)
  }
  function clear() {
    detail.value = null
  }
  return { detail, load, clear }
}
