<script setup>
import { ref } from 'vue'
import { useRequest as useApi } from '../../composables'

const selectedDate = ref('')
const { data: apod, loading, error, run } = useApi({ immediate: true, url: '/apod' })

function handleSearch() {
  const path = selectedDate.value ? `/apod?date=${selectedDate.value}` : '/apod'
  run(path)
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Foto do Dia</h1>
    </header>

    <!-- Seletor de data -->
    <form @submit.prevent="handleSearch" class="rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 mb-6">
      <div class="flex items-end gap-3">
        <div class="flex flex-col gap-1.5">
          <label class="text-[10px] uppercase tracking-widest text-white/35">Data</label>
          <input
            v-model="selectedDate"
            type="date"
            max="2026-06-11"
            min="1995-06-16"
            class="w-44 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm outline-none focus:border-white/20 font-mono [color-scheme:dark]"
          />
        </div>
        <button
          type="submit"
          class="px-6 py-2.5 bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm rounded-lg hover:bg-blue-500/30 transition-colors"
        >
          Buscar
        </button>
        <button
          v-if="selectedDate"
          type="button"
          @click="selectedDate = ''; handleSearch()"
          class="px-4 py-2.5 text-white/40 text-sm hover:text-white/60 transition-colors"
        >
          Hoje
        </button>
      </div>
    </form>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="apod">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[75vh]">
        <!-- Informações à esquerda -->
        <div class="flex flex-col justify-center space-y-6 overflow-y-auto pr-4">
          <h2 class="text-xl md:text-3xl font-bold leading-snug">{{ apod.title }}</h2>
          <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-white/80">
            <span>{{ apod.date }}</span>
            <span v-if="apod.copyright">© {{ apod.copyright }}</span>
          </div>
          <p class="text-sm text-white/70 leading-relaxed">{{ apod.explanation }}</p>
        </div>

        <!-- Imagem à direita -->
        <div class="rounded-2xl border border-white/[0.08] overflow-hidden h-full">
          <img
            v-if="apod.media_type === 'image'"
            :src="apod.url"
            :alt="apod.title"
            class="w-full h-full object-cover"
          />
          <iframe
            v-else-if="apod.media_type === 'video'"
            :src="apod.url"
            class="w-full h-full"
            allowfullscreen
          />
        </div>
      </div>
    </template>
  </div>
</template>