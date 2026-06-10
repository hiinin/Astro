<script setup>
import { useRouter } from 'vue-router'
import { useApi } from '../../composables/useApi.js'

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
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Asteroides</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Asteroides</h1>
      <p class="text-sm text-white/40">Dados fornecidos pela NASA NeoWs.</p>
    </header>

    <div v-if="asteroids === null" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <div v-else class="rounded-xl border border-white/[0.08] overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
            <th class="px-5 py-3 font-medium">Nome</th>
            <th class="px-5 py-3 font-medium">Magnitude</th>
            <th class="px-5 py-3 font-medium">Diâmetro est. (km)</th>
            <th class="px-5 py-3 font-medium">Risco</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="asteroid in asteroids"
            :key="asteroid.id"
            class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.03] cursor-pointer transition-colors"
            @click="router.push(`/asteroides/${asteroid.id}`)"
          >
            <td class="px-5 py-3.5 font-medium">{{ asteroid.name }}</td>
            <td class="px-5 py-3.5 text-white/60">{{ asteroid.absolute_magnitude_h }}</td>
            <td class="px-5 py-3.5 text-white/60">
              {{ asteroid.estimated_diameter?.kilometers?.estimated_diameter_min?.toFixed(3) }}
              –
              {{ asteroid.estimated_diameter?.kilometers?.estimated_diameter_max?.toFixed(3) }}
            </td>
            <td class="px-5 py-3.5">
              <span
                v-if="asteroid.is_potentially_hazardous_asteroid"
                class="text-xs font-medium px-2 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/20"
              >
                Perigoso
              </span>
              <span v-else class="text-white/25 text-xs">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>
