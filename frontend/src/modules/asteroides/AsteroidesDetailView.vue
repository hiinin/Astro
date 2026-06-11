<script setup>
import { useRoute } from 'vue-router'
import { useApi } from '../../composables/useApi.js'

const route = useRoute()

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

const { data: asteroid, loading, error } = useApi({
  immediate: true,
  url: () => `/neo/lookup/${route.params.id}`,
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="asteroid">
      <!-- Header -->
      <div class="flex items-start justify-between gap-6 mb-6">
        <div>
          <div class="flex items-center gap-3 mb-1.5">
            <h1 class="text-2xl font-bold">{{ asteroid.name }}</h1>
            <span v-if="asteroid.is_potentially_hazardous_asteroid"
              class="text-[11px] font-semibold px-2.5 py-1 rounded-full border border-orange-500/40 bg-orange-500/10 text-orange-400">
              ⚠ Perigoso
            </span>
            <span v-else
              class="text-[11px] font-semibold px-2.5 py-1 rounded-full border border-green-500/30 bg-green-500/10 text-green-400">
              Seguro
            </span>
          </div>
          <p class="text-xs text-white/35">ID: {{ asteroid.id }} · Designação: {{ asteroid.designation }} · Dados NASA NeoWs</p>
        </div>
        <a :href="jplUrl(asteroid.id)" target="_blank"
          class="flex items-center gap-1.5 text-xs border border-white/15 px-3 py-1.5 rounded-lg hover:bg-white/5 transition-colors shrink-0">
          Ver no JPL/NASA
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M1.5 8.5L8.5 1.5M8.5 1.5H4M8.5 1.5v4.5" />
          </svg>
        </a>
      </div>

      <!-- Tabela de identificação + métricas -->
      <div class="rounded-2xl border border-white/[0.08] overflow-hidden mb-4">
        <table class="w-full text-xs">
          <thead>
            <tr class="bg-white/[0.04] border-b border-white/[0.08] text-white/40 font-medium uppercase tracking-widest text-[10px]">
              <th class="px-5 py-3 text-left" colspan="2">Identificação &amp; Classificação</th>
              <th class="px-5 py-3 text-center">Magnitude Absoluta (H)</th>
              <th class="px-5 py-3 text-left">Classe Orbital</th>
              <th class="px-5 py-3 text-left" colspan="2">Diâmetro Estimado</th>
            </tr>
          </thead>
          <tbody>
            <!-- Linha 1 -->
            <tr class="border-b border-white/[0.05] hover:bg-white/[0.02] transition-colors">
              <td class="px-5 py-3 text-white/35 w-28">Nome</td>
              <td class="px-5 py-3 text-white/80 font-medium">{{ asteroid.name }}</td>
              <td class="px-5 py-3 text-center align-middle" rowspan="4">
                <p class="text-5xl font-bold tracking-tight text-white mb-1">{{ asteroid.absolute_magnitude_h }}</p>
                <p class="text-[11px] text-white/40">{{ magnitudeLabel(asteroid.absolute_magnitude_h) }}</p>
              </td>
              <td class="px-5 py-3 align-top" rowspan="4">
                <p class="text-white/80 font-medium mb-1">
                  {{ asteroid.orbital_data?.orbit_class?.orbit_class_type ?? '—' }}
                </p>
                <p class="text-white/35 leading-relaxed text-[11px]">
                  {{ asteroid.orbital_data?.orbit_class?.orbit_class_description ?? '—' }}
                </p>
              </td>
              <td class="px-5 py-3 text-white/35 w-8">km</td>
              <td class="px-5 py-3 font-mono text-white/60">
                {{ fmt(asteroid.estimated_diameter?.kilometers?.estimated_diameter_min) }}
                <span class="text-white/25">–</span>
                {{ fmt(asteroid.estimated_diameter?.kilometers?.estimated_diameter_max) }}
              </td>
            </tr>
            <!-- Linha 2 -->
            <tr class="border-b border-white/[0.05] hover:bg-white/[0.02] transition-colors">
              <td class="px-5 py-3 text-white/35">ID</td>
              <td class="px-5 py-3 text-white/80 font-medium">{{ asteroid.id }}</td>
              <td class="px-5 py-3 text-white/35">m</td>
              <td class="px-5 py-3 font-mono text-white/60">
                {{ fmt(asteroid.estimated_diameter?.meters?.estimated_diameter_min) }}
                <span class="text-white/25">–</span>
                {{ fmt(asteroid.estimated_diameter?.meters?.estimated_diameter_max) }}
              </td>
            </tr>
            <!-- Linha 3 -->
            <tr class="border-b border-white/[0.05] hover:bg-white/[0.02] transition-colors">
              <td class="px-5 py-3 text-white/35">Tipo</td>
              <td class="px-5 py-3 text-white/80 font-medium">NEO <span class="text-white/35 font-normal">· Near Earth Object</span></td>
              <td class="px-5 py-3 text-white/35">mi</td>
              <td class="px-5 py-3 font-mono text-white/60">
                {{ fmt(asteroid.estimated_diameter?.miles?.estimated_diameter_min) }}
                <span class="text-white/25">–</span>
                {{ fmt(asteroid.estimated_diameter?.miles?.estimated_diameter_max) }}
              </td>
            </tr>
            <!-- Linha 4 -->
            <tr class="hover:bg-white/[0.02] transition-colors">
              <td class="px-5 py-3 text-white/35">Perigoso</td>
              <td class="px-5 py-3">
                <span v-if="asteroid.is_potentially_hazardous_asteroid"
                  class="text-[11px] font-semibold px-2 py-0.5 rounded-full border border-orange-500/40 bg-orange-500/10 text-orange-400">
                  ⚠ Sim
                </span>
                <span v-else
                  class="text-[11px] font-semibold px-2 py-0.5 rounded-full border border-green-500/30 bg-green-500/10 text-green-400">
                  Não
                </span>
              </td>
              <td class="px-5 py-3 text-white/35">ft</td>
              <td class="px-5 py-3 font-mono text-white/60">
                {{ fmt(asteroid.estimated_diameter?.feet?.estimated_diameter_min) }}
                <span class="text-white/25">–</span>
                {{ fmt(asteroid.estimated_diameter?.feet?.estimated_diameter_max) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Tabela de aproximações -->
      <div class="rounded-2xl border border-white/[0.08] overflow-hidden mb-4">
        <div class="flex items-center justify-between px-5 py-3 bg-white/[0.04] border-b border-white/[0.08]">
          <p class="text-[10px] uppercase tracking-widest text-white/40 font-medium">Aproximações Próximas</p>
          <span class="text-xs text-white/25">{{ asteroid.close_approach_data?.length ?? 0 }} registros</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr class="text-white/30 border-b border-white/[0.06] uppercase tracking-widest text-[10px]">
                <th class="px-5 py-3 text-left font-medium">Data</th>
                <th class="px-5 py-3 text-left font-medium">Data/Hora UTC</th>
                <th class="px-5 py-3 text-left font-medium">Corpo</th>
                <th class="px-5 py-3 text-right font-medium">Vel. km/s</th>
                <th class="px-5 py-3 text-right font-medium">Vel. km/h</th>
                <th class="px-5 py-3 text-right font-medium">Dist. UA</th>
                <th class="px-5 py-3 text-right font-medium">Dist. Lunar</th>
                <th class="px-5 py-3 text-right font-medium">Dist. km</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(approach, i) in asteroid.close_approach_data" :key="i"
                class="border-b border-white/[0.04] last:border-0 hover:bg-white/[0.03] transition-colors">
                <td class="px-5 py-3 text-white/70 font-medium">{{ approach.close_approach_date }}</td>
                <td class="px-5 py-3 text-white/40">{{ approach.close_approach_date_full }}</td>
                <td class="px-5 py-3 text-white/60">{{ approach.orbiting_body }}</td>
                <td class="px-5 py-3 text-right font-mono text-white/60">{{ fmt(approach.relative_velocity?.kilometers_per_second) }}</td>
                <td class="px-5 py-3 text-right font-mono text-white/60">{{ fmt(approach.relative_velocity?.kilometers_per_hour) }}</td>
                <td class="px-5 py-3 text-right font-mono text-white/60">{{ fmt(approach.miss_distance?.astronomical, 10) }}</td>
                <td class="px-5 py-3 text-right font-mono text-white/60">{{ fmt(approach.miss_distance?.lunar) }}</td>
                <td class="px-5 py-3 text-right font-mono text-white/60">{{ fmt(approach.miss_distance?.kilometers) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Rodapé -->
      <div class="flex items-center justify-between px-1 py-2">
        <p class="text-xs text-white/25">Este objeto é um NEO com aproximações registradas ao longo dos séculos XX e XXI. Dados calculados pela NASA NeoWs.</p>
        <p class="text-xs text-white/20 shrink-0 ml-6">Atualizado em {{ new Date().toLocaleDateString('pt-BR') }}</p>
      </div>

    </template>
  </div>
</template>