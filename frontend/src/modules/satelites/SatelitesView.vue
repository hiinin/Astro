<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRequest as useApi } from '../../composables'

const router = useRouter()
const query = ref('')
const { data: results, loading, error, searched, search } = useApi()

function handleSearch() {
  if (!query.value.trim()) return
  search(`/tle?search=${encodeURIComponent(query.value)}`)
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Satélites</h1>
    </header>

    <form @submit.prevent="handleSearch" class="flex gap-3 mb-6">
      <input
        v-model="query"
        placeholder="Ex: ISS, Hubble, Starlink..."
        class="flex-1 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
      />
      <button
        type="submit"
        class="px-5 py-2.5 bg-red-500/20 border border-red-500/30 text-orange-300 text-sm rounded-lg hover:bg-blue-red/30 transition-colors"
      >
        Buscar
      </button>
    </form>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <p v-else-if="searched && results?.length === 0" class="text-sm text-white/40 py-8">
      Nenhum satélite encontrado para "{{ query }}".
    </p>

    <div v-else-if="results?.length" class="grid grid-cols-4 gap-3">
      <div
        v-for="sat in results.slice(0, 50)"
        :key="sat.NORAD_CAT_ID"
        class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex flex-col gap-4 hover:bg-white/[0.05] transition-colors cursor-pointer"
        @click="router.push(`/satelites/${sat.NORAD_CAT_ID}`)"
      >
        <div class="flex items-start justify-between gap-2">
          <p class="text-sm font-semibold leading-tight text-white">{{ sat.OBJECT_NAME }}</p>
          <span class="text-[10px] font-mono text-violet-400 bg-violet-500/10 border border-violet-500/20 px-1.5 py-0.5 rounded shrink-0">
            {{ sat.NORAD_CAT_ID }}
          </span>
        </div>

        <div class="flex flex-col gap-2 mt-auto">
          <div class="flex justify-between items-center">
            <span class="text-[10px] uppercase tracking-widest text-white/30">Inclinação</span>
            <span class="text-xs font-mono text-cyan-400">
              {{ sat.INCLINATION != null ? `${Number(sat.INCLINATION).toFixed(2)}°` : '—' }}
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-[10px] uppercase tracking-widest text-white/30">Época</span>
            <span class="text-xs text-amber-400/80">{{ sat.EPOCH?.split('T')[0] ?? '—' }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-[10px] uppercase tracking-widest text-white/30">Órbita</span>
            <span class="text-xs text-emerald-400/80">{{ sat.CLASSIFICATION_TYPE ?? '—' }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!searched" class="text-center py-16">
      <p class="text-white/30 text-sm">Digite o nome de um satélite para buscar.</p>
    </div>
  </div>
</template>