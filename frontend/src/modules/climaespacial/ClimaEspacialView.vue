<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../../composables/useApi.js'

const tab = ref('cme')
const { data, loading, error, run } = useApi()

const tabs = [
  { id: 'cme', label: 'Ejeções de Massa Coronal', endpoint: '/donki/cme' },
  { id: 'flr', label: 'Erupções Solares', endpoint: '/donki/flr' },
  { id: 'gst', label: 'Tempestades Geomagnéticas', endpoint: '/donki/gst' },
  { id: 'notifications', label: 'Notificações', endpoint: '/donki/notifications' },
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
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Clima Espacial</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Clima Espacial</h1>
      <p class="text-sm text-white/40">Eventos solares e geomagnéticos via NASA DONKI.</p>
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

    <p v-else-if="data?.length === 0" class="text-sm text-white/40 py-8">
      Nenhum evento recente encontrado.
    </p>

    <div v-else-if="data" class="rounded-xl border border-white/[0.08] overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
            <th class="px-5 py-3 font-medium">ID</th>
            <th class="px-5 py-3 font-medium">Início</th>
            <th class="px-5 py-3 font-medium">Tipo</th>
            <th class="px-5 py-3 font-medium">Observação</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, i) in data.slice(0, 30)"
            :key="i"
            class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.02]"
          >
            <td class="px-5 py-3 text-white/40 text-xs font-mono">{{ item.activityID ?? item.notificationID ?? `#${i + 1}` }}</td>
            <td class="px-5 py-3 text-white/60">{{ item.beginTime ?? item.startTime ?? item.messageIssueTime ?? '—' }}</td>
            <td class="px-5 py-3">
              <span class="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20">
                {{ item.cmeAnalyses?.[0]?.type ?? item.classType ?? item.kpIndex ?? tab.toUpperCase() }}
              </span>
            </td>
            <td class="px-5 py-3 text-white/50 text-xs max-w-xs truncate">{{ item.note ?? item.messageBody ?? '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
