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
      <!-- Imagem em destaque com texto sobreposto -->
      <div class="relative rounded-2xl border border-white/[0.08] overflow-hidden mb-6">
        <img
          v-if="apod.media_type === 'image'"
          :src="apod.url"
          :alt="apod.title"
          class="w-full h-[75vh] object-cover"
        />
        <iframe
          v-else-if="apod.media_type === 'video'"
          :src="apod.url"
          class="w-full h-[75vh]"
          allowfullscreen
        />

        <!-- Overlay com gradiente e textos em cima da foto -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent flex flex-col justify-end p-8">
          <p class="text-xl md:text-3xl font-bold leading-snug mb-3">{{ apod.title }}</p>
          <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-white/80 mb-4">
            <span>{{ apod.date }}</span>
            <span v-if="apod.copyright">© {{ apod.copyright }}</span>
          </div>
          <p class="text-sm text-white/70 leading-relaxed max-w-4xl">{{ apod.explanation }}</p>
        </div>
      </div>
    </template>
  </div>
</template>