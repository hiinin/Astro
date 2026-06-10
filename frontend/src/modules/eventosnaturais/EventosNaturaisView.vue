<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '../../composables/useApi.js'

const router = useRouter()
const search = ref('')
const { data: events, loading, error } = useApi({
  immediate: true,
  url: '/eonet/events?limit=100',
  transform: (data) => data.events ?? data ?? [],
})

const categoryColors = {
  'Wildfires': 'text-orange-400 bg-orange-500/10 border-orange-500/20',
  'Severe Storms': 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  'Volcanoes': 'text-red-400 bg-red-500/10 border-red-500/20',
  'Floods': 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20',
  'Earthquakes': 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',
}

function categoryClass(event) {
  const title = event.categories?.[0]?.title ?? ''
  return categoryColors[title] ?? 'text-white/40 bg-white/5 border-white/10'
}

const filtered = () =>
  (events.value ?? []).filter(e =>
    e.title?.toLowerCase().includes(search.value.toLowerCase()) ||
    e.categories?.[0]?.title?.toLowerCase().includes(search.value.toLowerCase())
  )
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Eventos Naturais</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Eventos Naturais</h1>
      <p class="text-sm text-white/40">Eventos naturais ao redor da Terra via NASA EONET.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="events">
      <input
        v-model="search"
        placeholder="Buscar por nome ou categoria..."
        class="w-full mb-5 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
      />

      <div class="rounded-xl border border-white/[0.08] overflow-hidden">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
              <th class="px-5 py-3 font-medium">Evento</th>
              <th class="px-5 py-3 font-medium">Categoria</th>
              <th class="px-5 py-3 font-medium">Data</th>
              <th class="px-5 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="event in filtered().slice(0, 60)"
              :key="event.id"
              class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.02] cursor-pointer transition-colors"
              @click="router.push(`/eventos-naturais/${event.id}`)"
            >
              <td class="px-5 py-3.5 font-medium">{{ event.title }}</td>
              <td class="px-5 py-3.5">
                <span class="text-xs px-2 py-0.5 rounded border" :class="categoryClass(event)">
                  {{ event.categories?.[0]?.title ?? '—' }}
                </span>
              </td>
              <td class="px-5 py-3.5 text-white/50 text-xs">
                {{ event.geometry?.[0]?.date?.split('T')[0] ?? '—' }}
              </td>
              <td class="px-5 py-3.5">
                <span
                  class="text-xs px-2 py-0.5 rounded border"
                  :class="event.closed
                    ? 'text-white/30 bg-white/5 border-white/10'
                    : 'text-green-400 bg-green-500/10 border-green-500/20'"
                >
                  {{ event.closed ? 'Encerrado' : 'Ativo' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
