<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../../composables/useApi.js'

const tab = ref('fireball')
const { data, loading, error, run } = useApi()

const tabs = [
  { id: 'fireball', label: 'Bolas de Fogo', endpoint: '/ssd/fireball', key: 'data', fields: ['date', 'energy', 'impact-e', 'lat', 'lon', 'alt', 'vel'] },
  { id: 'cad', label: 'Aproximações', endpoint: '/ssd/cad', key: 'data', fields: ['des', 'cd', 'dist', 'dist-min', 'v-rel', 'h', 'body'] },
  { id: 'sentry', label: 'Risco de Impacto', endpoint: '/ssd/sentry', key: 'data', fields: ['des', 'fullname', 'ip', 'ps_max', 'last_obs', 'v_inf'] },
]

function cellValue(row, field, index) {
  if (Array.isArray(row)) return row[index] ?? '—'
  return row[field] ?? '—'
}

function fetchTab(id) {
  tab.value = id
  const t = tabs.find(x => x.id === id)
  run(t.endpoint, { transform: (json) => json[t.key] ?? json })
}

const currentTab = () => tabs.find(t => t.id === tab.value)

onMounted(() => fetchTab('fireball'))
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Sistema Solar</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Sistema Solar</h1>
      <p class="text-sm text-white/40">Dados de bolas de fogo, aproximações e riscos de impacto via NASA SSD/CNEOS.</p>
    </header>

    <div class="flex gap-2 mb-6">
      <button
        v-for="t in tabs"
        :key="t.id"
        @click="fetchTab(t.id)"
        class="text-xs px-3 py-1.5 rounded-lg border transition-colors"
        :class="tab === t.id
          ? 'border-blue-500/50 bg-blue-500/10 text-blue-300'
          : 'border-white/10 text-white/50 hover:text-white/80 hover:border-white/20'"
      >
        {{ t.label }}
      </button>
    </div>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <p v-else-if="!data?.length" class="text-sm text-white/40 py-8">Sem dados disponíveis.</p>

    <div v-else class="rounded-xl border border-white/[0.08] overflow-x-auto">
      <table class="w-full text-xs">
        <thead>
          <tr class="border-b border-white/[0.08] text-left text-white/40 uppercase tracking-wider">
            <th v-for="field in currentTab()?.fields" :key="field" class="px-4 py-3 font-medium whitespace-nowrap">
              {{ field }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, i) in data.slice(0, 40)"
            :key="i"
            class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.02]"
          >
            <td
              v-for="(field, fi) in currentTab()?.fields"
              :key="field"
              class="px-4 py-3 text-white/60 whitespace-nowrap"
              :class="fi === 0 ? 'font-medium text-white/80' : ''"
            >
              {{ cellValue(row, field, fi) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
