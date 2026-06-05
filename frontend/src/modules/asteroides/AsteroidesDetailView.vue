<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const asteroid = ref(null)
const loading = ref(true)
const error = ref(null)

const diametro = [
  { label: 'km', key: 'kilometers' },
  { label: 'm', key: 'meters' },
  { label: 'mi', key: 'miles' },
  { label: 'ft', key: 'feet' },
]

const jplUrl = (id) => `https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=${id}`
const fmt = (n, decimals = 4) => Number(n).toFixed(decimals)

function magnitudeLabel(h) {
  if (h < 18) return 'Asteroide muito grande.'
  if (h < 22) return 'Asteroide relativamente pequeno.'
  return 'Asteroide pequeno.'
}

async function fetchAsteroid() {
  try {
    const res = await fetch(`/api/neo/lookup/${route.params.id}`)
    if (!res.ok) throw new Error(res.status)
    asteroid.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

fetchAsteroid()
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="asteroid">
      <div class="flex items-start justify-between gap-6 mb-6">
        <div>
          <nav class="mb-3 text-xs text-white/40">
            <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
            <span> › </span>
            <router-link to="/asteroides" class="hover:text-white/70 transition-colors">Asteroides</router-link>
            <span> › {{ asteroid.id }}</span>
          </nav>
          <h1 class="text-4xl font-bold mb-2">{{ asteroid.name }}</h1>
          <p class="text-sm text-white/50">ID: {{ asteroid.id }} · Designação: {{ asteroid.designation }}</p>
        </div>
        <a :href="jplUrl(asteroid.id)" target="_blank"
          class="shrink-0 flex items-center gap-1.5 text-xs border border-white/15 px-3 py-1.5 rounded-lg hover:bg-white/5 transition-colors mt-1">
          Documentação da API
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M1.5 8.5L8.5 1.5M8.5 1.5H4M8.5 1.5v4.5" />
          </svg>
        </a>
      </div>

      <div class="flex items-center gap-3 mb-2">
        <a :href="jplUrl(asteroid.id)" target="_blank"
          class="flex items-center gap-1.5 text-xs border border-white/15 px-3 py-1.5 rounded-lg hover:bg-white/5 transition-colors">
          Ver no JPL/NASA
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M1.5 8.5L8.5 1.5M8.5 1.5H4M8.5 1.5v4.5" />
          </svg>
        </a>
        <span v-if="asteroid.is_potentially_hazardous_asteroid"
          class="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg border border-orange-500/40 bg-orange-500/10 text-orange-400">
          ⚠ Potencialmente Perigoso
        </span>
      </div>
      <p class="text-xs text-white/35 mb-8">Dados fornecidos pela NASA NeoWs.</p>

      <div class="grid grid-cols-3 gap-4 mb-4">
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-4">Diâmetro Estimado</p>
          <dl class="space-y-2.5 text-xs text-white/70">
            <div v-for="unit in diametro" :key="unit.label">
              <span class="text-white/35">{{ unit.label }} </span>
              {{ fmt(asteroid.estimated_diameter?.[unit.key]?.estimated_diameter_min) }} – {{
                fmt(asteroid.estimated_diameter?.[unit.key]?.estimated_diameter_max) }}
            </div>
          </dl>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-4">Magnitude Absoluta (H)</p>
          <p class="text-5xl font-bold mb-2">{{ asteroid.absolute_magnitude_h }}</p>
          <p class="text-xs text-white/40">{{ magnitudeLabel(asteroid.absolute_magnitude_h) }}</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-4">Referência NASA/JPL</p>
          <a :href="jplUrl(asteroid.id)" target="_blank" class="text-xs text-blue-400 hover:underline break-all">{{
            jplUrl(asteroid.id) }}</a>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-4 mb-8">
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Tipo de Asteroide</p>
          <p class="text-sm">NEO (Near Earth Object)</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Potencialmente Perigoso</p>
          <p class="text-sm font-medium"
            :class="asteroid.is_potentially_hazardous_asteroid ? 'text-red-400' : 'text-green-400'">
            {{ asteroid.is_potentially_hazardous_asteroid ? 'Sim' : 'Não' }}
          </p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Links</p>
          <div v-for="(url, key) in asteroid.links" :key="key" class="text-xs">
            <span class="text-white/35">{{ key }}: </span>
            <a :href="url" target="_blank" class="text-blue-400 hover:underline break-all">{{ url }}</a>
          </div>
        </div>
      </div>

      <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] overflow-hidden mb-6">
        <p class="px-5 py-4 border-b border-white/[0.08] text-[11px] uppercase tracking-widest text-white/40">Dados de
          Aproximações Próximas</p>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr class="text-white/35 border-b border-white/[0.08]">
                <th class="px-4 py-2.5 text-left font-medium">Data</th>
                <th class="px-4 py-2.5 text-left font-medium">Data e Hora (UTC)</th>
                <th class="px-4 py-2.5 text-left font-medium">Corpo</th>
                <th class="px-4 py-2.5 text-right font-medium">Vel. km/s</th>
                <th class="px-4 py-2.5 text-right font-medium">Vel. km/h</th>
                <th class="px-4 py-2.5 text-right font-medium">Dist. UA</th>
                <th class="px-4 py-2.5 text-right font-medium">Dist. Lunar</th>
                <th class="px-4 py-2.5 text-right font-medium">Dist. km</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(approach, i) in asteroid.close_approach_data" :key="i"
                class="border-b border-white/[0.04] last:border-0 hover:bg-white/[0.02]">
                <td class="px-4 py-3 text-white/60">{{ approach.close_approach_date }}</td>
                <td class="px-4 py-3 text-white/60">{{ approach.close_approach_date_full }}</td>
                <td class="px-4 py-3 text-white/60">{{ approach.orbiting_body }}</td>
                <td class="px-4 py-3 text-right text-white/60">{{ fmt(approach.relative_velocity?.kilometers_per_second)
                  }}</td>
                <td class="px-4 py-3 text-right text-white/60">{{ fmt(approach.relative_velocity?.kilometers_per_hour)
                  }}</td>
                <td class="px-4 py-3 text-right text-white/60">{{ fmt(approach.miss_distance?.astronomical, 10) }}</td>
                <td class="px-4 py-3 text-right text-white/60">{{ fmt(approach.miss_distance?.lunar) }}</td>
                <td class="px-4 py-3 text-right text-white/60">{{ fmt(approach.miss_distance?.kilometers) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
        <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Sobre este Asteroide</p>
        <p class="text-sm text-white/55 mb-1">Este objeto é um asteroide próximo da Terra (NEO) com aproximações
          registradas ao longo do século XX e XXI.</p>
        <p class="text-xs text-white/35">Os dados acima são fornecidos pela NASA NeoWs e representam cálculos e
          previsões.</p>
        <p class="text-xs text-white/25 mt-4 text-right">Última atualização: {{ new Date().toLocaleDateString('pt-BR')
          }}</p>
      </div>

    </template>
  </div>
</template>
