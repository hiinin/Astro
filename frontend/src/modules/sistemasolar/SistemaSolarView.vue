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

const fieldColors = {
  // datas
  date:     'text-amber-400/80',
  cd:       'text-amber-400/80',
  last_obs: 'text-amber-400/80',
  // coordenadas / distâncias
  lat:      'text-cyan-400',
  lon:      'text-cyan-400',
  dist:     'text-cyan-400',
  'dist-min': 'text-cyan-300',
  // energia / velocidade
  energy:   'text-orange-400',
  'impact-e': 'text-orange-300',
  vel:      'text-violet-400',
  'v-rel':  'text-violet-400',
  v_inf:    'text-violet-400',
  // risco
  ip:       'text-red-400',
  ps_max:   'text-red-300',
  // altitude / magnitude
  alt:      'text-sky-400',
  h:        'text-sky-400',
  // corpo / classificação
  body:     'text-emerald-400/80',
}

function cellClass(field, index) {
  if (index === 0) return 'text-white font-medium'
  return fieldColors[field] ?? 'text-white/50'
}

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
      <h1 class="text-4xl font-bold mb-1">Sistema Solar</h1>
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

    <div v-else class="grid grid-cols-4 gap-4">
      <div
        v-for="(row, i) in data.slice(0, 40)"
        :key="i"
        class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-4 flex flex-col justify-between hover:bg-white/[0.06] transition-colors"
      >
        <div class="text-sm font-semibold text-white truncate">
          {{ cellValue(row, currentTab()?.fields[0], 0) }}
        </div>
        <div class="flex flex-col gap-1 mt-2 overflow-hidden">
          <div
            v-for="(field, fi) in currentTab()?.fields.slice(1)"
            :key="field"
            class="flex items-center justify-between text-xs font-mono"
          >
            <span class="text-white/40 uppercase tracking-wider truncate mr-2">{{ field }}</span>
            <span :class="cellClass(field, fi + 1)" class="truncate text-right">
              {{ cellValue(row, field, fi + 1) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>