<script setup>
import { useRoute } from 'vue-router'
import { useRequest as useApi } from '../../composables'

const route = useRoute()
const fmt = (n, d = 4) => (n != null ? Number(n).toFixed(d) : '—')

const { data: sat, loading, error } = useApi({
  immediate: true,
  url: () => `/tle/${route.params.id}`,
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="sat">
      <header class="mb-8">
        <h1 class="text-3xl font-bold mb-2">{{ sat.OBJECT_NAME }}</h1>
        <p class="text-sm text-white/40">NORAD {{ sat.NORAD_CAT_ID }} · {{ sat.OBJECT_ID }}</p>
      </header>

      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Inclinação</p>
          <p class="text-3xl font-bold">{{ fmt(sat.INCLINATION, 2) }}°</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Excentricidade</p>
          <p class="text-3xl font-bold">{{ fmt(sat.ECCENTRICITY, 5) }}</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Movimento médio</p>
          <p class="text-3xl font-bold">{{ fmt(sat.MEAN_MOTION, 4) }}</p>
          <p class="text-xs text-white/40 mt-1">rev/dia</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Época</p>
          <p class="text-sm font-medium">{{ sat.EPOCH?.split('T')[0] ?? '—' }}</p>
          <p class="text-xs text-white/40 mt-1 font-mono">{{ sat.EPOCH?.split('T')[1]?.slice(0, 12) ?? '' }}</p>
        </div>
      </div>

      <div class="rounded-xl border border-white/[0.08] overflow-hidden">
        <p class="px-5 py-4 border-b border-white/[0.08] text-[11px] uppercase tracking-widest text-white/40">
          Elementos orbitais (TLE)
        </p>
        <table class="w-full text-xs">
          <tbody>
            <tr
              v-for="row in [
                ['Classificação', sat.CLASSIFICATION_TYPE],
                ['Ascensão reta do nó', `${fmt(sat.RA_OF_ASC_NODE, 4)}°`],
                ['Argumento do perigeu', `${fmt(sat.ARG_OF_PERICENTER, 4)}°`],
                ['Anomalia média', `${fmt(sat.MEAN_ANOMALY, 4)}°`],
                ['Revoluções na época', sat.REV_AT_EPOCH],
                ['Termo de arrasto (B*)', fmt(sat.BSTAR, 8)],
                ['Derivada do mov. médio', fmt(sat.MEAN_MOTION_DOT, 8)],
                ['Segunda derivada', fmt(sat.MEAN_MOTION_DDOT, 8)],
                ['Tipo de efemérides', sat.EPHEMERIS_TYPE],
                ['Conjunto de elementos', sat.ELEMENT_SET_NO],
              ]"
              :key="row[0]"
              class="border-b border-white/[0.04] last:border-0"
            >
              <td class="px-5 py-3 text-white/40 w-1/3">{{ row[0] }}</td>
              <td class="px-5 py-3 text-white/70 font-mono">{{ row[1] ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
