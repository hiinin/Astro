<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../../composables/useApi.js'

const tab = ref('cme')
const { data, loading, error, run } = useApi()

const tabs = [
  { id: 'cme',           label: 'Ejeções Coronais',      endpoint: '/donki/cme' },
  { id: 'flr',           label: 'Erupções Solares',       endpoint: '/donki/flr' },
  { id: 'gst',           label: 'Tempestades Geomag.',    endpoint: '/donki/gst' },
  { id: 'notifications', label: 'Notificações',           endpoint: '/donki/notifications' },
]

function fetchTab(id) {
  tab.value = id
  const endpoint = tabs.find(t => t.id === id)?.endpoint
  run(endpoint, {
    transform: (json) => (Array.isArray(json) ? json : (json.items ?? [])),
  })
}

onMounted(() => fetchTab('cme'))
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Clima Espacial</h1>
    </header>

    <!-- Tabs em cards -->
    <div class="grid grid-cols-4 gap-3 mb-8">
      <button
        v-for="t in tabs"
        :key="t.id"
        @click="fetchTab(t.id)"
        class="flex flex-col items-start gap-2 rounded-xl border px-4 py-3.5 text-left transition-colors"
        :class="tab === t.id
          ? 'border-blue-500/40 bg-blue-500/10 text-blue-200'
          : 'border-white/[0.08] bg-white/[0.02] text-white/50 hover:bg-white/[0.04] hover:text-white/70'"
      >
        <span class="text-xs font-medium leading-snug">{{ t.label }}</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <!-- Erro -->
    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <!-- Vazio -->
    <p v-else-if="data?.length === 0" class="text-sm text-white/40 py-8">
      Nenhum evento recente encontrado.
    </p>

    <!-- Cards de itens -->
    <div v-else-if="data" class="flex flex-col gap-3">
      <div
        v-for="(item, i) in data.slice(0, 30)"
        :key="i"
        class="flex items-center gap-6 rounded-xl border border-white/[0.08] bg-white/[0.03] px-5 py-4 hover:bg-white/[0.05] transition-colors"
      >
        <!-- Badge tipo -->
        <div class="shrink-0">
          <span class="text-xs px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-300 border border-blue-500/20 font-mono font-medium">
            {{ item.cmeAnalyses?.[0]?.type ?? item.classType ?? item.kpIndex ?? tab.toUpperCase() }}
          </span>
        </div>

        <!-- ID + observação -->
        <div class="flex-1 min-w-0">
          <p class="text-xs font-mono text-white/35 mb-0.5 truncate">
            {{ item.activityID ?? item.notificationID ?? `#${i + 1}` }}
          </p>
          <p class="text-sm text-white/60 truncate">
            {{ item.note ?? item.messageBody ?? '—' }}
          </p>
        </div>

        <!-- Data -->
        <div class="shrink-0 flex flex-col gap-0.5 text-right">
          <span class="text-[10px] uppercase tracking-widest text-white/30">Início</span>
          <span class="text-xs text-white/55 font-mono">
            {{ item.beginTime ?? item.startTime ?? item.messageIssueTime ?? '—' }}
          </span>
        </div>
      </div>
    </div>

  </div>
</template>