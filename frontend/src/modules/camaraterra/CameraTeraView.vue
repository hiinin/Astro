<script setup>
import { epicDateOf, epicImageUrl, useEpic } from '../../composables'
import { tabClass } from '../../composables'

const { tab, tabs, data, loading, error, dateDetail, mode, isDates, dateKind, switchTab, loadDate } = useEpic()
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Câmera da Terra</h1>
      <p class="text-sm text-white/40">Imagens da Terra capturadas pela câmera DSCOVR/EPIC — natural e enhanced.</p>
    </header>

    <!-- Tabs -->
    <div class="flex gap-2 mb-6 flex-wrap">
      <button v-for="t in tabs" :key="t.id" :class="tabClass(tab === t.id)" @click="switchTab(t.id)">
        {{ t.label }}
      </button>
    </div>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <!-- Dates mode -->
    <div v-else-if="isDates() && data?.length" class="grid grid-cols-4 gap-3">
      <button
        v-for="d in data.slice(0, 32)"
        :key="epicDateOf(d)"
        class="text-xs text-white/50 px-3 py-2 rounded-lg border border-white/[0.08] hover:border-white/20 text-left transition-colors"
        @click="loadDate(d)"
      >{{ epicDateOf(d) }}</button>
    </div>

    <!-- Images mode -->
    <div v-else-if="data?.length" class="grid grid-cols-4 gap-4">
      <div v-for="img in data.slice(0, 12)" :key="img.identifier" class="rounded-xl border border-white/[0.08] overflow-hidden">
        <img
          :src="epicImageUrl(img, mode())"
          :alt="img.caption"
          loading="lazy"
          class="w-full aspect-square object-cover"
        />
        <div class="p-3">
          <p class="text-xs text-white/60 truncate">{{ img.caption }}</p>
          <p class="text-[10px] text-white/30 mt-1">{{ img.date?.split(' ')[0] }}</p>
        </div>
      </div>
    </div>

    <p v-else class="text-sm text-white/40 py-8">Nenhuma imagem disponível.</p>

    <!-- Date detail images -->
    <div v-if="dateDetail?.length" class="mt-6 grid grid-cols-4 gap-4">
      <div v-for="img in dateDetail.slice(0, 8)" :key="img.identifier" class="rounded-xl border border-white/[0.08] overflow-hidden">
        <img
          :src="epicImageUrl(img, dateKind())"
          :alt="img.caption"
          loading="lazy"
          class="w-full aspect-square object-cover"
        />
        <p class="p-3 text-xs text-white/60 truncate">{{ img.caption }}</p>
      </div>
    </div>
  </div>
</template>