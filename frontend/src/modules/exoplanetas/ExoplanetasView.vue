<script setup>
import { ref, computed } from 'vue'
import { useApi } from '../../composables/useApi.js'

const search = ref('')
const viewMode = ref('grid') // 'grid' | 'list'
const sortBy = ref('disc_year')
const selectedMethod = ref('')

const { data: planets, loading, error } = useApi({
  immediate: true,
  url: '/exoplanet?table=pscomppars&select=pl_name,hostname,disc_year,discoverymethod,pl_orbper,pl_rade,pl_bmasse,sy_dist,pl_eqt&limit=200&format=json',
})

const methods = computed(() => {
  const set = new Set((planets.value ?? []).map(p => p.discoverymethod).filter(Boolean))
  return [...set].sort()
})

const filtered = computed(() => {
  let list = (planets.value ?? []).filter(p =>
    p.pl_name?.toLowerCase().includes(search.value.toLowerCase()) ||
    p.hostname?.toLowerCase().includes(search.value.toLowerCase())
  )
  if (selectedMethod.value) {
    list = list.filter(p => p.discoverymethod === selectedMethod.value)
  }
  list.sort((a, b) => {
    const va = a[sortBy.value]
    const vb = b[sortBy.value]
    if (va == null && vb == null) return 0
    if (va == null) return 1
    if (vb == null) return -1
    return vb > va ? 1 : vb < va ? -1 : 0
  })
  return list
})

const stats = computed(() => {
  const all = planets.value ?? []
  const avgRadius = all.filter(p => p.pl_rade != null).reduce((s, p) => s + Number(p.pl_rade), 0) / (all.filter(p => p.pl_rade != null).length || 1)
  const avgMass = all.filter(p => p.pl_bmasse != null).reduce((s, p) => s + Number(p.pl_bmasse), 0) / (all.filter(p => p.pl_bmasse != null).length || 1)
  const maxDist = Math.max(...all.filter(p => p.sy_dist != null).map(p => Number(p.sy_dist)), 0)
  return { total: all.length, avgRadius, avgMass, maxDist }
})

const fmt = (n, d = 2) => n != null ? Number(n).toFixed(d) : '—'

const sizeClass = (radius) => {
  if (radius == null) return 'size-8'
  if (radius < 1.5) return 'size-6'
  if (radius < 4) return 'size-9'
  if (radius < 10) return 'size-12'
  return 'size-16'
}

const colorClass = (temp) => {
  if (temp == null) return 'from-gray-500 to-gray-700'
  if (temp < 300) return 'from-blue-400 to-blue-700'
  if (temp < 700) return 'from-green-400 to-teal-600'
  if (temp < 1500) return 'from-yellow-400 to-orange-600'
  return 'from-red-400 to-red-700'
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <!-- Header -->
    <header class="mb-8">
      <div class="flex items-end justify-between">
        <div>
          <h1 class="text-4xl font-bold mb-2 bg-white bg-clip-text text-transparent">
            Exoplanetas
          </h1>
        </div>
        <!-- View toggle -->
        <div class="flex items-center gap-1 bg-white/[0.04] border border-white/[0.08] rounded-lg p-1">
          <button
            @click="viewMode = 'grid'"
            :class="['px-3 py-1.5 text-xs rounded-md transition-all', viewMode === 'grid' ? 'bg-purple-500/20 text-purple-300' : 'text-white/40 hover:text-white/60']"
          >
            ⊞ Grid
          </button>
          <button
            @click="viewMode = 'list'"
            :class="['px-3 py-1.5 text-xs rounded-md transition-all', viewMode === 'list' ? 'bg-purple-500/20 text-purple-300' : 'text-white/40 hover:text-white/60']"
          >
            ☰ Lista
          </button>
        </div>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center gap-4 py-24">
      <span class="size-10 rounded-full border-2 border-white/10 border-t-purple-400 animate-spin" />
      <p class="text-sm text-white/40">Buscando exoplanetas...</p>
    </div>

    <!-- Error -->
    <p v-else-if="error" class="text-sm text-red-400 py-16 text-center">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="planets">
      <!-- Stats Cards -->
      <div class="grid grid-cols-4 gap-4 mb-8">
        <div class="bg-white/[0.03] border border-white/[0.08] rounded-xl p-5">
          <p class="text-xs text-white/40 uppercase tracking-wider mb-1">Total</p>
          <p class="text-2xl font-bold text-purple-300">{{ stats.total }}</p>
          <p class="text-[11px] text-white/30 mt-1">planetas catalogados</p>
        </div>
        <div class="bg-white/[0.03] border border-white/[0.08] rounded-xl p-5">
          <p class="text-xs text-white/40 uppercase tracking-wider mb-1">Raio Médio</p>
          <p class="text-2xl font-bold text-blue-300">{{ fmt(stats.avgRadius, 1) }}</p>
          <p class="text-[11px] text-white/30 mt-1">R⊕ (raios terrestres)</p>
        </div>
        <div class="bg-white/[0.03] border border-white/[0.08] rounded-xl p-5">
          <p class="text-xs text-white/40 uppercase tracking-wider mb-1">Massa Média</p>
          <p class="text-2xl font-bold text-green-300">{{ fmt(stats.avgMass, 1) }}</p>
          <p class="text-[11px] text-white/30 mt-1">M⊕ (massas terrestres)</p>
        </div>
        <div class="bg-white/[0.03] border border-white/[0.08] rounded-xl p-5">
          <p class="text-xs text-white/40 uppercase tracking-wider mb-1">Mais Distante</p>
          <p class="text-2xl font-bold text-orange-300">{{ fmt(stats.maxDist, 0) }}</p>
          <p class="text-[11px] text-white/30 mt-1">parsecs</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="flex items-center gap-4 mb-6">
        <input
          v-model="search"
          placeholder="Buscar planeta ou estrela..."
          class="flex-1 max-w-sm bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-purple-500/40 transition-colors"
        />
        
        <p class="text-xs text-white/40 ml-auto">{{ filtered.length }} resultados</p>
      </div>

      <!-- Grid View -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-3 gap-4">
        <div
          v-for="p in filtered.slice(0, 60)"
          :key="p.pl_name"
          class="group bg-white/[0.02] border border-white/[0.08] rounded-xl p-5 hover:bg-white/[0.04] hover:border-purple-500/20 transition-all duration-300"
        >
          <div class="flex items-start gap-4">
            <!-- Planet visual -->
            <div class="flex-shrink-0 flex items-center justify-center w-16 h-16">
              <div
                :class="[sizeClass(p.pl_rade), 'rounded-full bg-gradient-to-br shadow-lg', colorClass(p.pl_eqt)]"
              />
            </div>
            <!-- Info -->
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-sm truncate group-hover:text-purple-200 transition-colors">{{ p.pl_name }}</h3>
              <p class="text-xs text-white/40 mt-0.5">{{ p.hostname ?? '—' }}</p>
              <div class="mt-2">
                <span class="inline-block px-2 py-0.5 rounded text-[10px] bg-purple-500/10 text-purple-300 border border-purple-500/20">
                  {{ p.discoverymethod ?? '—' }}
                </span>
                <span v-if="p.disc_year" class="ml-2 text-[10px] text-white/30">{{ p.disc_year }}</span>
              </div>
            </div>
          </div>
          <!-- Metrics -->
          <div class="grid grid-cols-3 gap-3 mt-4 pt-4 border-t border-white/[0.06]">
            <div>
              <p class="text-[10px] text-white/30 uppercase">Raio</p>
              <p class="text-xs font-mono text-white/70">{{ fmt(p.pl_rade) }} R⊕</p>
            </div>
            <div>
              <p class="text-[10px] text-white/30 uppercase">Massa</p>
              <p class="text-xs font-mono text-white/70">{{ fmt(p.pl_bmasse) }} M⊕</p>
            </div>
            <div>
              <p class="text-[10px] text-white/30 uppercase">Dist.</p>
              <p class="text-xs font-mono text-white/70">{{ fmt(p.sy_dist, 0) }} pc</p>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="flex flex-col gap-2">
        <div
          v-for="p in filtered.slice(0, 60)"
          :key="p.pl_name"
          class="flex items-center gap-5 bg-white/[0.02] border border-white/[0.08] rounded-lg px-5 py-3.5 hover:bg-white/[0.04] hover:border-purple-500/20 transition-all duration-300"
        >
          <div
            :class="['flex-shrink-0 rounded-full bg-gradient-to-br', sizeClass(p.pl_rade), colorClass(p.pl_eqt)]"
          />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ p.pl_name }}</p>
            <p class="text-xs text-white/40">{{ p.hostname ?? '—' }}</p>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] bg-purple-500/10 text-purple-300 border border-purple-500/20">
            {{ p.discoverymethod ?? '—' }}
          </span>
          <div class="flex gap-6 text-xs font-mono text-white/50">
            <span>{{ p.disc_year ?? '—' }}</span>
            <span>{{ fmt(p.pl_rade) }} R⊕</span>
            <span>{{ fmt(p.pl_bmasse) }} M⊕</span>
            <span>{{ fmt(p.sy_dist, 0) }} pc</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
