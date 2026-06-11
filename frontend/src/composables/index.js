/**
 * Barrel export — importa tudo de um lugar só.
 *
 * Uso:
 *   import { useRequest, apiFetch, useTabs, tabClass } from '@/composables'
 *   import { useEpic, epicImageUrl } from '@/composables'
 *   import { useOsdr } from '@/composables'
 */

// ─── API (core HTTP + composables genéricos) ────────────────────────────
export { apiFetch } from './api/client.js'
export { useRequest, useFetchDetail } from './api/useRequest.js'
export { useTabs, tabClass } from './api/useTabs.js'

// ─── NASA (dados específicos das APIs da NASA) ──────────────────────────
export { DONKI_TABS, donkiStart, donkiId, donkiNote } from './nasa/useDonki.js'
export { useEpic, epicImageUrl, epicDateOf, EPIC_TABS } from './nasa/useEpic.js'
export { useEarthImagery } from './nasa/useEarthImagery.js'
export {
  useMedia, mediaThumb, mediaAssetUrl, mediaVideoUrl,
  mediaIsVideo, mediaAssetFiles, mediaParseError,
} from './nasa/useMedia.js'

// ─── Science (repositórios de ciência aberta) ───────────────────────────
export {
  useOsdr, itemKey, osdPagePath, osdDetailTitle, osdLinkedItem,
  osdParentLinks, osdRows, osdDetailRows, OSDR_TABS, OSDR_TYPE_LABELS,
} from './science/useOsdr.js'

// ─── Scene (3D / visualizações) ─────────────────────────────────────────
export { useEarthGlobe } from './scene/useEarthGlobe.js'
