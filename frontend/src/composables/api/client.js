/**
 * Core HTTP client — responsável por montar URLs e fazer fetch genérico.
 */

function buildUrl(path) {
  if (path.startsWith('http')) return path
  if (path.startsWith('/api')) return path
  return `/api${path.startsWith('/') ? path : `/${path}`}`
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

/**
 * Fetch simplificado que já resolve a URL do proxy backend.
 * @param {string} path - caminho relativo (/earth/imagery) ou absoluto
 * @param {object} options - { parseErrorDetail }
 */
export async function apiFetch(path, options = {}) {
  const res = await fetch(buildUrl(path))
  return parseResponse(res, options)
}
