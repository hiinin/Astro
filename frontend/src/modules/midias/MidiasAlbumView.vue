<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '../../composables'
import { mediaThumb, mediaParseError } from '../../composables'

const route = useRoute()
const router = useRouter()
const albumId = decodeURIComponent(route.params.id)

const items = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const data = await apiFetch(`/images/album/${encodeURIComponent(albumId)}`)
    items.value = data.collection?.items ?? []
  } catch (e) {
    error.value = mediaParseError(e.message) ?? e.message
  } finally {
    loading.value = false
  }
})

function openMedia(item) {
  const d = item.data?.[0]
  if (d?.nasa_id) router.push({ path: `/midias/${d.nasa_id}`, query: { title: d.title } })
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-2xl font-bold mb-1">Álbum: {{ albumId }}</h1>
      <p class="text-xs text-white/35">NASA Image & Video Library</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando álbum...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">{{ error }}</p>

    <p v-else-if="!items.length" class="text-sm text-white/40 py-8">Álbum vazio ou não encontrado.</p>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
      <div
        v-for="(item, i) in items.slice(0, 40)"
        :key="i"
        class="group rounded-2xl border border-white/[0.07] bg-white/[0.02] overflow-hidden cursor-pointer hover:border-white/[0.15] hover:bg-white/[0.04] transition-all duration-300"
        @click="openMedia(item)"
      >
        <div class="aspect-[4/3] bg-white/[0.03] flex items-center justify-center overflow-hidden">
          <img
            v-if="mediaThumb(item)"
            :src="mediaThumb(item)"
            :alt="item.data?.[0]?.title"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
          <span v-else class="text-white/20 text-xs">Sem prévia</span>
        </div>
        <div class="p-4">
          <p class="text-xs font-medium text-white/80 line-clamp-2 leading-snug mb-2">{{ item.data?.[0]?.title }}</p>
          <span class="text-[10px] text-white/30">{{ item.data?.[0]?.date_created?.split('T')[0] }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
