/**
 * Composable para busca e exibição de mídias do NASA Image & Video Library.
 */
import { ref, onMounted } from 'vue'
import { useRequest } from '../api/useRequest.js'

export function mediaThumb(item) {
  return (item.links ?? []).find(
    (l) => l.rel === 'preview' || /\.(jpg|png)$/i.test(l.href ?? ''),
  )?.href ?? null
}

export function mediaAssetUrl(asset) {
  const items = asset?.collection?.items ?? []
  for (const size of ['~large.jpg', '~medium.jpg', '~orig.jpg', '~large.', '~medium.', '~orig.']) {
    const hit = items.find((i) => i.href?.includes(size) && /\.(jpg|png|webp)/i.test(i.href))
    if (hit) return hit.href.replace(/^http:/, 'https:')
  }
  return items.find((i) => /\.(jpg|png|webp)/i.test(i.href ?? ''))?.href?.replace(/^http:/, 'https:') ?? null
}

export function mediaVideoUrl(asset) {
  const items = asset?.collection?.items ?? []
  for (const key of ['~medium.mp4', '~preview.mp4', '~mobile.mp4']) {
    const hit = items.find((i) => i.href?.includes(key))
    if (hit) return hit.href.replace(/^http:/, 'https:')
  }
  return items.find((i) => /\.mp4$/i.test(i.href ?? ''))?.href?.replace(/^http:/, 'https:') ?? null
}

export function mediaIsVideo(asset) {
  return (asset?.collection?.items ?? []).some((i) => /\.mp4|\.mov|\/video\//i.test(i.href ?? ''))
}

export function mediaAssetFiles(asset) {
  return (asset?.collection?.items ?? [])
    .map((i) => i.href?.replace(/^http:/, 'https:'))
    .filter((h) => h && !h.endsWith('metadata.json') && !h.endsWith('.vtt'))
}

export function mediaParseError(msg) {
  if (!msg) return msg
  if (msg.includes('No assets found for album')) {
    const m = msg.match(/album=\\"([^\\"]+)\\"/)
    return `Álbum "${m?.[1] ?? 'informado'}" não encontrado. Use o ID exato (case-sensitive).`
  }
  return msg.replace(/^Erro retornado pela API externa \(\d+\):\s*/, '')
}

export function useMedia() {
  const query = ref('Saturn')
  const { data: results, loading, error, searched, search } = useRequest({ initialData: [] })

  function handleSearch() {
    if (!query.value.trim()) return
    search(`/images/search?q=${encodeURIComponent(query.value)}&media_type=image`, {
      transform: (data) => data.collection?.items ?? [],
    })
  }

  onMounted(handleSearch)

  return { query, results, loading, error, searched, handleSearch }
}
