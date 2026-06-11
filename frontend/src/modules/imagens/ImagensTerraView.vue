<script setup>
import { useEarthImagery } from '../../composables'

const { lat, lon, dim, date, minDate, maxDate, result, loading, error, searched, handleSearch } = useEarthImagery()
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Imagens da Terra</h1>
    </header>

    <!-- Formulário -->
    <form @submit.prevent="handleSearch" class="rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 mb-6">
      <p class="text-[10px] uppercase tracking-widest text-white/35 mb-4 font-medium">Parâmetros de busca</p>
      <div class="flex items-end gap-3">
        <div class="flex flex-col gap-1.5">
          <label class="text-[10px] uppercase tracking-widest text-white/35">Latitude</label>
          <input
            v-model="lat"
            placeholder="-23.5"
            class="w-36 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20 font-mono"
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="text-[10px] uppercase tracking-widest text-white/35">Longitude</label>
          <input
            v-model="lon"
            placeholder="-46.6"
            class="w-36 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20 font-mono"
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="text-[10px] uppercase tracking-widest text-white/35">Dimensão (°)</label>
          <input
            v-model="dim"
            placeholder="1"
            class="w-28 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20 font-mono"
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="text-[10px] uppercase tracking-widest text-white/35">Data</label>
          <input
            v-model="date"
            type="date"
            :min="minDate"
            :max="maxDate"
            class="w-40 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20 font-mono [color-scheme:dark]"
          />
        </div>
        <button
          type="submit"
          class="px-6 py-2.5 bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm rounded-lg hover:bg-blue-500/30 transition-colors"
        >
          Buscar
        </button>
      </div>
    </form>

    <!-- Datas disponíveis -->
    <p v-if="minDate && maxDate" class="text-xs text-white/35 mb-6">
      Datas disponíveis: {{ minDate }} até {{ maxDate }}
    </p>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Gerando imagem...
    </div>

    <!-- Erro -->
    <p v-else-if="error" class="text-sm text-red-400 py-8">
      Falha ao carregar ({{ error }}). Verifique as coordenadas ou tente novamente.
    </p>

    <!-- Resultado -->
    <template v-else-if="result?.url">
      <div class="rounded-2xl border border-white/[0.08] overflow-hidden">

        <!-- Imagem em destaque -->
        <div class="relative w-full bg-black" style="aspect-ratio: 16/7;">
          <img
            :src="result.url"
            alt="Imagem de satélite"
            class="w-full h-full object-cover"
          />
          <div class="absolute bottom-0 left-0 right-0 px-5 py-3 bg-gradient-to-t from-black/70 to-transparent">
            <p class="text-xs text-white/60">MODIS Terra · NASA Earthdata</p>
          </div>
        </div>

        <!-- Metadados em tabela -->
        <table class="w-full text-xs border-t border-white/[0.08]">
          <thead>
            <tr class="bg-white/[0.04] border-b border-white/[0.08] text-white/40 uppercase tracking-widest text-[10px] font-medium">
              <th class="px-5 py-3 text-left">Data</th>
              <th class="px-5 py-3 text-left">Latitude</th>
              <th class="px-5 py-3 text-left">Longitude</th>
              <th class="px-5 py-3 text-left">Dimensão</th>
              <th class="px-5 py-3 text-left">Fonte</th>
            </tr>
          </thead>
          <tbody>
            <tr class="hover:bg-white/[0.02] transition-colors">
              <td class="px-5 py-3 text-white/70 font-medium">{{ result.date ?? '—' }}</td>
              <td class="px-5 py-3 font-mono text-white/60">{{ lat }}°</td>
              <td class="px-5 py-3 font-mono text-white/60">{{ lon }}°</td>
              <td class="px-5 py-3 font-mono text-white/60">{{ dim }}°</td>
              <td class="px-5 py-3 text-white/35">GIBS / NASA Earthdata</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- Sem resultado -->
    <p v-else-if="searched" class="text-sm text-white/40 py-8">
      Nenhuma imagem encontrada para essas coordenadas.
    </p>

    <!-- Estado inicial -->
    <div v-else class="rounded-2xl border border-white/[0.05] border-dashed py-20 flex flex-col items-center gap-3 text-center">
      <svg class="text-white/20" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
        <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/>
        <line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/>
        <line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/>
      </svg>
      <p class="text-sm text-white/30">Informe latitude e longitude e clique em Buscar.</p>
    </div>

  </div>
</template>