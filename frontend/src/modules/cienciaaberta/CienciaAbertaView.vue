<script setup>
import { ref, onMounted } from 'vue'

const tab = ref('missions')
const data = ref(null)
const loading = ref(false)
const error = ref(null)

const tabs = [
  { id: 'missions', label: 'Missões', endpoint: '/api/osdr/missions' },
  { id: 'experiments', label: 'Experimentos', endpoint: '/api/osdr/experiments' },
  { id: 'payloads', label: 'Payloads', endpoint: '/api/osdr/payloads' },
]

async function fetchTab(id) {
  tab.value = id
  data.value = null
  loading.value = true
  error.value = null
  const endpoint = tabs.find(t => t.id === id)?.endpoint
  try {
    const res = await fetch(endpoint)
    if (!res.ok) throw new Error(res.status)
    const json = await res.json()
    data.value = Array.isArray(json) ? json : (json.results ?? json.content ?? Object.values(json)[0] ?? [])
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchTab('missions'))
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Ciência Aberta</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Ciência Aberta</h1>
      <p class="text-sm text-white/40">Missões, experimentos e payloads via NASA OSDR.</p>
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

    <div v-else class="grid grid-cols-2 gap-4">
      <div
        v-for="(item, i) in data.slice(0, 30)"
        :key="item.identifier ?? i"
        class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5"
      >
        <p class="font-semibold text-sm mb-1 truncate">{{ item.title ?? item.name ?? item.identifier ?? `#${i + 1}` }}</p>
        <p v-if="item.identifier" class="text-[10px] font-mono text-white/30 mb-2">{{ item.identifier }}</p>
        <p v-if="item.description" class="text-xs text-white/55 line-clamp-3 leading-relaxed">{{ item.description }}</p>
        <div v-if="item.start_date ?? item.startDate" class="mt-3 text-[11px] text-white/35">
          {{ item.start_date ?? item.startDate }}
          <span v-if="item.end_date ?? item.endDate"> — {{ item.end_date ?? item.endDate }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
