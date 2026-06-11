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
      <div class="rounded-2xl border border-white/[0.08] overflow-hidden flex">

        <!-- Informações à esquerda -->
        <div class="flex-1 p-6 flex flex-col justify-center gap-5">
          <h2 class="text-lg font-semibold text-white/90">Detalhes da Imagem</h2>

          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <span class="text-[10px] uppercase tracking-widest text-white/35 font-medium">Data</span>
              <span class="text-sm text-white/70 font-medium">{{ result.date ?? '—' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-[10px] uppercase tracking-widest text-white/35 font-medium">Latitude</span>
              <span class="text-sm text-white/60 font-mono">{{ lat }}°</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-[10px] uppercase tracking-widest text-white/35 font-medium">Longitude</span>
              <span class="text-sm text-white/60 font-mono">{{ lon }}°</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-[10px] uppercase tracking-widest text-white/35 font-medium">Dimensão</span>
              <span class="text-sm text-white/60 font-mono">{{ dim }}°</span>
            </div>
          </div>

          <div class="flex flex-col gap-1 pt-2 border-t border-white/[0.06]">
            <span class="text-[10px] uppercase tracking-widest text-white/35 font-medium">Fonte</span>
            <span class="text-sm text-white/50">GIBS / NASA Earthdata</span>
          </div>

          <p class="text-xs text-white/30 mt-2">MODIS Terra · NASA Earthdata</p>
        </div>

        <!-- Imagem quadrada à direita -->
        <div class="w-[400px] h-[400px] flex-shrink-0 bg-black">
          <img
            :src="result.url"
            alt="Imagem de satélite"
            class="w-full h-full object-cover"
          />
        </div>

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