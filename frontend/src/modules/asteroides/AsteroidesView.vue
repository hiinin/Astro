<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRequest as useApi } from '../../composables'

const router = useRouter()

/* ── Estado de pesquisa por data ── */
const startDate = ref('')
const endDate = ref('')

/* ── Requisição: começa com browse, mas pode trocar para feed ── */
const { data: asteroids, loading, error, search } = useApi({
  immediate: true,
  url: '/neo/browse',
  transform: (data) => data.near_earth_objects ?? [],
})

/* ── Pesquisa por data (usa /neo/feed) ── */
const feedResult = ref(null)

const displayList = computed(() => {
  if (feedResult.value) return feedResult.value
  return asteroids.value ?? []
})

function searchByDate() {
  if (!startDate.value) return
  const end = endDate.value || startDate.value
  const url = `/neo/feed?start_date=${startDate.value}&end_date=${end}`

  search(url, {
    transform: (data) => {
      // /neo/feed retorna { near_earth_objects: { "2024-01-01": [...], ... } }
      const byDate = data.near_earth_objects ?? {}
      const flat = Object.values(byDate).flat()
      feedResult.value = flat
      return flat
    },
  })
}

function clearSearch() {
  startDate.value = ''
  endDate.value = ''
  feedResult.value = null
  search('/neo/browse', {
    transform: (data) => data.near_earth_objects ?? [],
  })
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <header class="mb-8">
      <div class="flex items-end justify-between">
        <div>
          <h1 class="text-4xl font-bold mb-1">Asteroides</h1>
        </div>
        <p v-if="displayList.length" class="text-xs text-white/25 mb-0.5">{{ displayList.length }} objetos</p>
      </div>

      <!-- Barra de pesquisa por data -->
      <div class="mt-5 flex flex-wrap items-end gap-3">
        <div class="flex flex-col gap-1">
          <label class="text-[11px] uppercase tracking-widest text-white/40">Data Inicial</label>
          <input
            v-model="startDate"
            type="date"
            class="rounded-lg border border-white/[0.1] bg-white/[0.04] px-3 py-2 text-sm text-white outline-none focus:border-blue-500/50 transition"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-[11px] uppercase tracking-widest text-white/40">Data Final</label>
          <input
            v-model="endDate"
            type="date"
            class="rounded-lg border border-white/[0.1] bg-white/[0.04] px-3 py-2 text-sm text-white outline-none focus:border-blue-500/50 transition"
          />
        </div>
        <button
          class="rounded-lg bg-blue-600/80 hover:bg-blue-600 px-4 py-2 text-sm font-medium transition disabled:opacity-40 disabled:cursor-not-allowed"
          :disabled="!startDate"
          @click="searchByDate"
        >
          Pesquisar
        </button>
        <button
          v-if="feedResult"
          class="rounded-lg border border-white/[0.1] px-4 py-2 text-sm text-white/60 hover:text-white hover:border-white/20 transition"
          @click="clearSearch"
        >
          Limpar
        </button>
      </div>
    </header>

    <!-- Erro -->
    <p v-if="error" class="text-red-400 text-sm mb-4">{{ error }}</p>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <!-- Lista -->
    <div v-else-if="displayList.length" class="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4">
      <div
        v-for="(asteroid, i) in displayList"
        :key="asteroid.id || asteroid.neo_reference_id"
        class="group relative rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 cursor-pointer hover:bg-white/[0.06] hover:border-white/[0.14] transition-all duration-200"
        @click="router.push(`/asteroides/${asteroid.id || asteroid.neo_reference_id}`)"
      >
        <!-- Topo: índice + badge de risco -->
        <div class="flex items-center justify-between mb-4">
          <span class="text-[11px] text-white/20 tabular-nums">{{ String(i + 1).padStart(2, '0') }}</span>
          <span
            v-if="asteroid.is_potentially_hazardous_asteroid"
            class="text-[11px] font-medium px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20"
          >
            Perigoso
          </span>
          <span v-else class="text-[11px] text-white/20 px-2 py-0.5 rounded-full border border-white/[0.06]">Seguro</span>
        </div>

        <!-- Nome -->
        <p class="font-semibold text-base leading-snug mb-5 truncate">{{ asteroid.name }}</p>

        <!-- Métricas -->
        <div class="grid grid-cols-2 gap-3">
          <div class="rounded-xl bg-white/[0.04] px-3 py-2.5">
            <p class="text-[11px] uppercase tracking-widest text-white/30 mb-1">Magnitude</p>
            <p class="text-sm font-mono text-white/80">{{ asteroid.absolute_magnitude_h }}</p>
          </div>
          <div class="rounded-xl bg-white/[0.04] px-3 py-2.5">
            <p class="text-[11px] uppercase tracking-widest text-white/30 mb-1">Diâmetro (km)</p>
            <p class="text-sm font-mono text-white/80">
              {{ asteroid.estimated_diameter?.kilometers?.estimated_diameter_min?.toFixed(2) }}
              <span class="text-white/30">–</span>
              {{ asteroid.estimated_diameter?.kilometers?.estimated_diameter_max?.toFixed(2) }}
            </p>
          </div>
        </div>

        <!-- Seta hover -->
        <div class="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity text-white/30 text-sm">→</div>
      </div>
    </div>

    <!-- Vazio -->
    <div v-else class="text-center text-white/30 py-16 text-sm">
      Nenhum asteroide encontrado para o período selecionado.
    </div>

  </div>
</template>
