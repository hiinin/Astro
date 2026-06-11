<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '../../composables'
import { mediaAssetUrl, mediaVideoUrl, mediaIsVideo, mediaAssetFiles, mediaParseError } from '../../composables'

const route = useRoute()
const nasaId = route.params.id
const title = route.query.title ?? nasaId

const asset = ref(null)
const imgUrl = ref(null)
const videoUrl = ref(null)
const isVideo = ref(false)
const files = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const data = await apiFetch(`/images/asset/${nasaId}`)
    asset.value = data
    imgUrl.value = mediaAssetUrl(data)
    videoUrl.value = mediaVideoUrl(data)
    isVideo.value = mediaIsVideo(data)
    files.value = mediaAssetFiles(data)
  } catch (e) {
    error.value = mediaParseError(e.message) ?? e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-2xl font-bold mb-1">{{ title }}</h1>
      <p class="text-xs text-white/35 font-mono">{{ nasaId }}</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando asset...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">{{ error }}</p>

    <template v-else>
      <!-- Vídeo -->
      <div v-if="isVideo && videoUrl" class="rounded-2xl border border-white/[0.08] overflow-hidden mb-6">
        <video :src="videoUrl" controls class="w-full max-h-[500px] bg-black" />
      </div>

      <!-- Imagem -->
      <div v-else-if="imgUrl" class="rounded-2xl border border-white/[0.08] overflow-hidden mb-6">
        <img :src="imgUrl" :alt="title" class="w-full max-h-[600px] object-contain bg-black" />
      </div>

      <p v-else class="text-sm text-white/40 py-8">Nenhuma mídia disponível para este asset.</p>

      <!-- Arquivos disponíveis -->
      <div v-if="files.length" class="rounded-xl border border-white/[0.08] bg-white/[0.02] p-5">
        <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Arquivos disponíveis ({{ files.length }})</p>
        <div class="flex flex-col gap-1.5 max-h-48 overflow-y-auto">
          <a
            v-for="(f, i) in files"
            :key="i"
            :href="f"
            target="_blank"
            class="text-xs text-blue-400 hover:text-blue-300 truncate transition-colors"
          >
            {{ f.split('/').pop() }}
          </a>
        </div>
      </div>
    </template>
  </div>
</template>
