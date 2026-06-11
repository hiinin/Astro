<script setup>
import { useRequest as useApi } from '../../composables'

const { data: apod, loading, error } = useApi({ immediate: true, url: '/apod' })
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-2xl font-bold mb-1">Foto do Dia</h1>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="apod">
      <!-- Imagem em destaque, full-width -->
      <div class="rounded-2xl border border-white/[0.08] overflow-hidden mb-6">
        <img
          v-if="apod.media_type === 'image'"
          :src="apod.url"
          :alt="apod.title"
          class="w-full h-[480px] object-cover"
        />
        <iframe
          v-else-if="apod.media_type === 'video'"
          :src="apod.url"
          class="w-full aspect-video"
          allowfullscreen
        />
      </div>

      <!-- Título + metadados em linha -->
      <div class="flex flex-wrap items-start gap-x-10 gap-y-3 mb-6 pb-6 border-b border-white/[0.08]">
        <div class="flex-1 min-w-[200px]">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-1">Título</p>
          <p class="text-xl font-bold leading-snug">{{ apod.title }}</p>
        </div>
        <div>
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-1">Data</p>
          <p class="text-sm text-white/80">{{ apod.date }}</p>
        </div>
        <div v-if="apod.copyright">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-1">Crédito</p>
          <p class="text-sm text-white/80">{{ apod.copyright }}</p>
        </div>
      </div>

      <!-- Descrição full-width -->
      <div>
        <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Descrição</p>
        <p class="text-sm text-white/70 leading-relaxed max-w-4xl">{{ apod.explanation }}</p>
      </div>
    </template>
  </div>
</template>