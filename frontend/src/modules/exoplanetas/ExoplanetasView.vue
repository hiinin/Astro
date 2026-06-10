<script setup>
import { ref, computed } from 'vue'
import { useApi } from '../../composables/useApi.js'

const search = ref('')
const { data: planets, loading, error } = useApi({
  immediate: true,
  url: '/exoplanet?table=pscomppars&select=pl_name,hostname,disc_year,discoverymethod,pl_orbper,pl_rade,pl_bmasse,sy_dist,pl_eqt&limit=200&format=json',
})

const filtered = computed(() =>
  (planets.value ?? []).filter(p =>
    p.pl_name?.toLowerCase().includes(search.value.toLowerCase()) ||
    p.hostname?.toLowerCase().includes(search.value.toLowerCase())
  )
)

const fmt = (n, d = 2) => n != null ? Number(n).toFixed(d) : '—'
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Exoplanetas</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Exoplanetas</h1>
      <p class="text-sm text-white/40">Catálogo de exoplanetas via NASA Exoplanet Archive.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="planets">
      <div class="flex items-center justify-between mb-5">
        <input
          v-model="search"
          placeholder="Buscar por planeta ou estrela hospedeira..."
          class="w-96 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
        />
        <p class="text-xs text-white/40">{{ filtered.length }} planetas</p>
      </div>

      <div class="rounded-xl border border-white/[0.08] overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
              <th class="px-5 py-3 font-medium">Planeta</th>
              <th class="px-5 py-3 font-medium">Estrela</th>
              <th class="px-5 py-3 font-medium">Descoberto</th>
              <th class="px-5 py-3 font-medium">Método</th>
              <th class="px-5 py-3 font-medium text-right">Período (dias)</th>
              <th class="px-5 py-3 font-medium text-right">Raio (R⊕)</th>
              <th class="px-5 py-3 font-medium text-right">Massa (M⊕)</th>
              <th class="px-5 py-3 font-medium text-right">Dist. (pc)</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="p in filtered.slice(0, 60)"
              :key="p.pl_name"
              class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.02]"
            >
              <td class="px-5 py-3.5 font-medium">{{ p.pl_name }}</td>
              <td class="px-5 py-3.5 text-white/60">{{ p.hostname ?? '—' }}</td>
              <td class="px-5 py-3.5 text-white/50">{{ p.disc_year ?? '—' }}</td>
              <td class="px-5 py-3.5 text-xs">
                <span class="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">
                  {{ p.discoverymethod ?? '—' }}
                </span>
              </td>
              <td class="px-5 py-3.5 text-right text-white/60 font-mono text-xs">{{ fmt(p.pl_orbper, 3) }}</td>
              <td class="px-5 py-3.5 text-right text-white/60 font-mono text-xs">{{ fmt(p.pl_rade) }}</td>
              <td class="px-5 py-3.5 text-right text-white/60 font-mono text-xs">{{ fmt(p.pl_bmasse) }}</td>
              <td class="px-5 py-3.5 text-right text-white/60 font-mono text-xs">{{ fmt(p.sy_dist) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
