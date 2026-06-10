<script setup>
import { ref } from 'vue'
import { useApi } from '../../composables/useApi.js'

const lat = ref('-23.5')
const lon = ref('-46.6')
const dim = ref('1')
const { data: result, loading, error, searched, search } = useApi()

function handleSearch() {
  const params = new URLSearchParams({
    lat: lat.value,
    lon: lon.value,
    dim: dim.value,
  })
  search(`/earth/imagery?${params}`)
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Imagens da Terra</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Imagens da Terra</h1>
      <p class="text-sm text-white/40">MODIS Terra (GIBS) — imagem por coordenada via NASA Earthdata.</p>
    </header>

    <form @submit.prevent="handleSearch" class="flex flex-wrap gap-3 mb-6">
      <input
        v-model="lat"
        placeholder="Latitude"
        class="w-32 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20"
      />
      <input
        v-model="lon"
        placeholder="Longitude"
        class="w-32 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20"
      />
      <input
        v-model="dim"
        placeholder="Dimensão (°)"
        class="w-32 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20"
      />
      <button
        type="submit"
        class="px-5 py-2.5 bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm rounded-lg hover:bg-blue-500/30 transition-colors"
      >
        Buscar
      </button>
    </form>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Gerando imagem...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-8">
      Falha ao carregar ({{ error }}). Verifique as coordenadas ou tente novamente.
    </p>

    <template v-else-if="result?.url">
      <div class="grid grid-cols-3 gap-6">
        <div class="rounded-xl border border-white/[0.05] overflow-hidden">
          <img :src="result.url" alt="Imagem de satélite" class="w-full object-cover bg-black" />
        </div>
        <div class="rounded-xl border border-white/[0.05] bg-white/[0.02] p-5 text-sm space-y-3">
          <div>
            <p class="text-[11px] uppercase tracking-widest text-white/40 mb-1">Data</p>
            <p>{{ result.date ?? '—' }}</p>
          </div>
          <div>
            <p class="text-[11px] uppercase tracking-widest text-white/40 mb-1">Coordenadas</p>
            <p>{{ lat }}, {{ lon }}</p>
          </div>
        </div>
      </div>
    </template>

    <p v-else-if="searched" class="text-sm text-white/40 py-8">Nenhuma imagem encontrada para essas coordenadas.</p>

    <p v-else class="text-sm text-white/30 py-16 text-center">
      Informe latitude e longitude e clique em Buscar.
    </p>
  </div>
</template>
