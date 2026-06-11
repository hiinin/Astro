<script setup>
import { useRouter } from 'vue-router'
import { useRequest as useApi } from '../../composables'

const router = useRouter()
const { data: asteroids } = useApi({
  immediate: true,
  url: '/neo/browse',
  transform: (data) => data.near_earth_objects ?? [],
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <header class="mb-8">
      <div class="flex items-end justify-between">
        <div>
          <h1 class="text-4xl font-bold mb-1">Asteroides</h1>
        </div>
        <p v-if="asteroids" class="text-xs text-white/25 mb-0.5">{{ asteroids.length }} objetos</p>
      </div>
    </header>

    <div v-if="asteroids === null" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <div v-else class="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4">
      <div
        v-for="(asteroid, i) in asteroids"
        :key="asteroid.id"
        class="group relative rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 cursor-pointer hover:bg-white/[0.06] hover:border-white/[0.14] transition-all duration-200"
        @click="router.push(`/asteroides/${asteroid.id}`)"
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

  </div>
</template>