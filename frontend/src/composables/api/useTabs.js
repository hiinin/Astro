/**
 * Composable de abas genérico — carrega dados ao trocar de tab.
 */
import { ref, onMounted } from 'vue'
import { useRequest } from './useRequest.js'

/**
 * @param {Array<{id, label, path, transform?}>} tabs
 */
export function useTabs(tabs) {
  const tab = ref(tabs[0]?.id)
  const { data, loading, error, run } = useRequest()

  function load(id = tab.value) {
    tab.value = id
    const current = tabs.find((t) => t.id === id)
    if (current) run(current.path, { transform: current.transform })
  }

  onMounted(() => load())

  return { tab, tabs, data, loading, error, load }
}

const TAB_BTN = 'text-xs px-3 py-1.5 rounded-lg border transition-colors'

export function tabClass(active) {
  return active
    ? `${TAB_BTN} border-blue-500/50 bg-blue-500/10 text-blue-300`
    : `${TAB_BTN} border-white/10 text-white/50 hover:text-white/80 hover:border-white/20`
}
