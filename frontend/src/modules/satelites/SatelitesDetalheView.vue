<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useRequest as useApi } from '../../composables'

const route = useRoute()
const router = useRouter()
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
      <!-- Botão voltar -->
      <button
        @click="router.push('/satelites')"
        class="flex items-center gap-2 text-sm text-white/40 hover:text-white/70 transition-colors mb-6"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        Voltar
      </button>

      <!-- Header com identidade do satélite -->
      <header class="relative rounded-2xl border border-white/[0.08] bg-gradient-to-br from-violet-500/10 via-transparent to-cyan-500/5 p-8 mb-8 overflow-hidden">
        <div class="absolute top-4 right-6">
          <span class="text-xs font-mono text-violet-400 bg-violet-500/10 border border-violet-500/20 px-3 py-1.5 rounded-full">
            NORAD {{ sat.NORAD_CAT_ID }}
          </span>
        </div>
        <h1 class="text-4xl font-bold mb-2">{{ sat.OBJECT_NAME }}</h1>
        <p class="text-sm text-white/50">{{ sat.OBJECT_ID }} · Classificação: {{ sat.CLASSIFICATION_TYPE ?? '—' }}</p>
        <p class="text-xs text-white/30 mt-2">Época: {{ sat.EPOCH?.replace('T', ' às ').slice(0, 22) ?? '—' }}</p>
      </header>

      <!-- Layout de duas colunas -->
      <div class="grid grid-cols-3 gap-6">
        <!-- Coluna principal: dados orbitais em grid -->
        <div class="col-span-2 space-y-6">
          <h2 class="text-xs uppercase tracking-widest text-white/40">Parâmetros orbitais</h2>

          <div class="grid grid-cols-3 gap-4">
            <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex flex-col">
              <span class="text-[10px] uppercase tracking-widest text-white/30 mb-2">Inclinação</span>
              <span class="text-2xl font-bold text-cyan-400">{{ fmt(sat.INCLINATION, 2) }}°</span>
            </div>
            <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex flex-col">
              <span class="text-[10px] uppercase tracking-widest text-white/30 mb-2">Excentricidade</span>
              <span class="text-2xl font-bold text-amber-400">{{ fmt(sat.ECCENTRICITY, 5) }}</span>
            </div>
            <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex flex-col">
              <span class="text-[10px] uppercase tracking-widest text-white/30 mb-2">Movimento médio</span>
              <span class="text-2xl font-bold text-emerald-400">{{ fmt(sat.MEAN_MOTION, 4) }}</span>
              <span class="text-[10px] text-white/30 mt-1">rev/dia</span>
            </div>
            <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex flex-col">
              <span class="text-[10px] uppercase tracking-widest text-white/30 mb-2">Ascensão reta (nó)</span>
              <span class="text-2xl font-bold text-violet-400">{{ fmt(sat.RA_OF_ASC_NODE, 2) }}°</span>
            </div>
            <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex flex-col">
              <span class="text-[10px] uppercase tracking-widest text-white/30 mb-2">Arg. do perigeu</span>
              <span class="text-2xl font-bold text-rose-400">{{ fmt(sat.ARG_OF_PERICENTER, 2) }}°</span>
            </div>
            <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex flex-col">
              <span class="text-[10px] uppercase tracking-widest text-white/30 mb-2">Anomalia média</span>
              <span class="text-2xl font-bold text-sky-400">{{ fmt(sat.MEAN_ANOMALY, 2) }}°</span>
            </div>
          </div>

          <!-- Tabela complementar -->
          <div class="rounded-xl border border-white/[0.08] overflow-hidden">
            <p class="px-5 py-3 border-b border-white/[0.08] text-[11px] uppercase tracking-widest text-white/40 bg-white/[0.02]">
              Dados complementares
            </p>
            <div class="divide-y divide-white/[0.04]">
              <div
                v-for="row in [
                  ['Termo de arrasto (B*)', fmt(sat.BSTAR, 8)],
                  ['Derivada do mov. médio', fmt(sat.MEAN_MOTION_DOT, 8)],
                  ['Segunda derivada', fmt(sat.MEAN_MOTION_DDOT, 8)],
                  ['Tipo de efemérides', sat.EPHEMERIS_TYPE],
                  ['Conjunto de elementos', sat.ELEMENT_SET_NO],
                ]"
                :key="row[0]"
                class="flex items-center justify-between px-5 py-3"
              >
                <span class="text-xs text-white/40">{{ row[0] }}</span>
                <span class="text-xs text-white/70 font-mono">{{ row[1] ?? '—' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Coluna lateral: resumo rápido -->
        <div class="space-y-4">
          <h2 class="text-xs uppercase tracking-widest text-white/40">Resumo</h2>

          <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 space-y-4">
            <div>
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Nome do objeto</p>
              <p class="text-sm font-semibold">{{ sat.OBJECT_NAME }}</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">ID do objeto</p>
              <p class="text-sm font-mono text-white/70">{{ sat.OBJECT_ID ?? '—' }}</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Catálogo NORAD</p>
              <p class="text-sm font-mono text-violet-400">{{ sat.NORAD_CAT_ID }}</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Classificação</p>
              <p class="text-sm text-white/70">{{ sat.CLASSIFICATION_TYPE ?? '—' }}</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Revoluções na época</p>
              <p class="text-sm font-mono text-white/70">{{ sat.REV_AT_EPOCH ?? '—' }}</p>
            </div>
          </div>

          <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
            <p class="text-[10px] uppercase tracking-widest text-white/30 mb-3">Época (data/hora)</p>
            <p class="text-sm font-medium">{{ sat.EPOCH?.split('T')[0] ?? '—' }}</p>
            <p class="text-xs font-mono text-white/40 mt-1">{{ sat.EPOCH?.split('T')[1]?.slice(0, 12) ?? '' }}</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
