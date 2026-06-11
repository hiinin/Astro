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

const categoryConfig = {
  'Wildfires':      { color: 'text-orange-400 bg-orange-500/10 border-orange-500/20', accent: 'bg-orange-500', bar: 'from-orange-500/30 to-transparent' },
  'Severe Storms':  { color: 'text-blue-400 bg-blue-500/10 border-blue-500/20',       accent: 'bg-blue-500',   bar: 'from-blue-500/30 to-transparent' },
  'Volcanoes':      { color: 'text-red-400 bg-red-500/10 border-red-500/20',           accent: 'bg-red-500',    bar: 'from-red-500/30 to-transparent' },
  'Floods':         { color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20',        accent: 'bg-cyan-500',   bar: 'from-cyan-500/30 to-transparent' },
  'Earthquakes':    { color: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',  accent: 'bg-yellow-500', bar: 'from-yellow-500/30 to-transparent' },
}

function cfg(event) {
  const title = event.categories?.[0]?.title ?? ''
  return categoryConfig[title] ?? { color: 'text-white/40 bg-white/5 border-white/10', accent: 'bg-white/20', bar: 'from-white/10 to-transparent' }
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
      <h1 class="text-4xl font-bold mb-1">Eventos Naturais</h1>
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
        class="w-full mb-6 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
      />

      <div class="grid grid-cols-4 gap-4">
        <div
          v-for="event in filtered().slice(0, 60)"
          :key="event.id"
          class="relative rounded-xl border border-white/[0.08] bg-white/[0.03] overflow-hidden cursor-pointer hover:border-white/[0.16] hover:bg-white/[0.05] transition-all flex flex-col"
          @click="router.push(`/eventos-naturais/${event.id}`)"
        >
          <!-- Gradiente de cor no topo -->
          <div class="h-16 w-full bg-gradient-to-b shrink-0" :class="cfg(event).bar">
            <div class="h-full flex items-start p-3">
              <!-- Dot indicador -->
              <div class="size-2 rounded-full mt-0.5 shrink-0" :class="cfg(event).accent" />
            </div>
          </div>

          <div class="px-4 pb-4 flex flex-col gap-3 flex-1">
            <!-- Título -->
            <p class="text-sm font-semibold text-white/90 leading-snug line-clamp-2 -mt-1">
              {{ event.title }}
            </p>

            <!-- Rodapé -->
            <div class="flex items-center justify-between mt-auto">
              <span class="text-[10px] px-2 py-0.5 rounded border" :class="cfg(event).color">
                {{ event.categories?.[0]?.title ?? '—' }}
              </span>
              <div class="flex items-center gap-2">
                <span
                  class="text-[10px] px-2 py-0.5 rounded border"
                  :class="event.closed
                    ? 'text-white/30 bg-white/5 border-white/10'
                    : 'text-green-400 bg-green-500/10 border-green-500/20'"
                >
                  {{ event.closed ? 'Encerrado' : 'Ativo' }}
                </span>
              </div>
            </div>

            <p class="text-[10px] text-white/30 font-mono -mt-1">
              {{ event.geometry?.[0]?.date?.split('T')[0] ?? '—' }}
            </p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>