<script setup>
import { ref, onMounted } from 'vue'

const apod = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/apod')
    if (!res.ok) throw new Error(res.status)
    apod.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Foto do Dia</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Foto do Dia</h1>
      <p class="text-sm text-white/40">Astronomy Picture of the Day — NASA APOD.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="apod">
      <div class="grid grid-cols-2 gap-6">
        <div class="rounded-xl border border-white/[0.08] overflow-hidden">
          <img
            v-if="apod.media_type === 'image'"
            :src="apod.url"
            :alt="apod.title"
            class="w-full object-cover"
          />
          <iframe
            v-else-if="apod.media_type === 'video'"
            :src="apod.url"
            class="w-full aspect-video"
            allowfullscreen
          />
        </div>

        <div class="flex flex-col gap-4">
          <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
            <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Título</p>
            <p class="text-xl font-bold">{{ apod.title }}</p>
          </div>
          <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
            <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Data</p>
            <p class="text-sm text-white/80">{{ apod.date }}</p>
          </div>
          <div v-if="apod.copyright" class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
            <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Crédito</p>
            <p class="text-sm text-white/80">{{ apod.copyright }}</p>
          </div>
          <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 flex-1">
            <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Descrição</p>
            <p class="text-sm text-white/70 leading-relaxed">{{ apod.explanation }}</p>
          </div>
          <a
            v-if="apod.hdurl"
            :href="apod.hdurl"
            target="_blank"
            class="flex items-center gap-1.5 text-xs border border-white/15 px-3 py-2 rounded-lg hover:bg-white/5 transition-colors w-fit"
          >
            Ver imagem em HD
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M1.5 8.5L8.5 1.5M8.5 1.5H4M8.5 1.5v4.5" />
            </svg>
          </a>
        </div>
      </div>
    </template>
  </div>
</template>
