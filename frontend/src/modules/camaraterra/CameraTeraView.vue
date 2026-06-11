<script setup>
import { epicDateOf, epicImageUrl, useEpic } from '../../composables'
import { tabClass } from '../../composables'

const { tab, tabs, data, loading, error, dateDetail, mode, isDates, dateKind, switchTab, loadDate } = useEpic()
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Câmera da Terra</h1>
    </header>

    <!-- Tabs reorganizados em linha compacta com select -->
    <div class="flex items-center gap-4 mb-6">
      <select
        :value="tab"
        @change="switchTab($event.target.value)"
        class="bg-white/[0.06] border border-white/[0.12] text-white text-sm rounded-lg px-4 py-2 outline-none focus:border-blue-400/60 transition-colors cursor-pointer"
      >
        <option v-for="t in tabs" :key="t.id" :value="t.id" class="bg-zinc-900 text-white">
          {{ t.label }}
        </option>
      </select>
      <span class="text-xs text-white/30">Selecione o tipo de visualização</span>
    </div>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <!-- Dates mode — compacto em chips inline -->
    <div v-else-if="isDates() && data?.length">
      <p class="text-xs text-white/40 mb-3">Clique em uma data para ver as imagens:</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="d in data.slice(0, 32)"
          :key="epicDateOf(d)"
          class="text-xs text-white/60 px-3 py-1.5 rounded-full bg-white/[0.05] border border-white/[0.1] hover:bg-white/[0.1] hover:border-white/20 transition-colors"
          @click="loadDate(d)"
        >{{ epicDateOf(d) }}</button>
      </div>
    </div>

    <!-- Images mode — cards de lista horizontal (metade do tamanho) -->
    <div v-else-if="data?.length" class="flex flex-col gap-3">
      <div
        v-for="img in data.slice(0, 12)"
        :key="img.identifier"
        class="flex items-center gap-4 rounded-xl border border-white/[0.08] overflow-hidden bg-white/[0.02] hover:bg-white/[0.04] transition-colors"
      >
        <img
          :src="epicImageUrl(img, mode())"
          :alt="img.caption"
          loading="lazy"
          class="w-24 h-24 object-cover flex-shrink-0"
        />
        <div class="py-3 pr-4 min-w-0">
          <p class="text-sm text-white/70 truncate">{{ img.caption }}</p>
          <p class="text-xs text-white/30 mt-1">{{ img.date?.split(' ')[0] }}</p>
        </div>
      </div>
    </div>

    <p v-else class="text-sm text-white/40 py-8">Nenhuma imagem disponível.</p>

    <!-- Date detail images — cards de lista horizontal -->
    <div v-if="dateDetail?.length" class="mt-6 flex flex-col gap-3">
      <div
        v-for="img in dateDetail.slice(0, 8)"
        :key="img.identifier"
        class="flex items-center gap-4 rounded-xl border border-white/[0.08] overflow-hidden bg-white/[0.02] hover:bg-white/[0.04] transition-colors"
      >
        <img
          :src="epicImageUrl(img, dateKind())"
          :alt="img.caption"
          loading="lazy"
          class="w-24 h-24 object-cover flex-shrink-0"
        />
        <div class="py-3 pr-4 min-w-0">
          <p class="text-sm text-white/70 truncate">{{ img.caption }}</p>
          <p class="text-xs text-white/30 mt-1">{{ img.date?.split(' ')[0] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>