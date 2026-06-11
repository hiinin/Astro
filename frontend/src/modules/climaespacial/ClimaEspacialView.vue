<script setup>
import { DONKI_TABS, donkiId, donkiNote, donkiStart } from '../../composables'
import { tabClass, useTabs } from '../../composables'

const { tab, tabs, data, loading, error, load } = useTabs(DONKI_TABS)
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Clima Espacial</h1>
    </header>

    <!-- Tabs em cards -->
    <div class="grid grid-cols-5 gap-3 mb-8">
      <button
        v-for="t in tabs"
        :key="t.id"
        @click="load(t.id)"
        :class="tabClass(tab === t.id)"
      >
        {{ t.label }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <!-- Erro -->
    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <!-- Vazio -->
    <p v-else-if="data?.length === 0" class="text-sm text-white/40 py-8">
      Nenhum evento recente encontrado.
    </p>

    <!-- Cards de itens -->
    <div v-else-if="data" class="flex flex-col gap-3">
      <div
        v-for="(item, i) in data.slice(0, 30)"
        :key="i"
        class="flex items-center gap-6 rounded-xl border border-white/[0.08] bg-white/[0.03] px-5 py-4 hover:bg-white/[0.05] transition-colors"
      >
        <!-- Badge tipo -->
        <div class="shrink-0">
          <span class="text-xs px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-300 border border-blue-500/20 font-mono font-medium">
            {{ tab.toUpperCase() }}
          </span>
        </div>

        <!-- ID + observação -->
        <div class="flex-1 min-w-0">
          <p class="text-xs font-mono text-white/35 mb-0.5 truncate">
            {{ donkiId(item, i) }}
          </p>
          <p class="text-sm text-white/60 truncate">
            {{ donkiNote(item) }}
          </p>
        </div>

        <!-- Data -->
        <div class="shrink-0 flex flex-col gap-0.5 text-right">
          <span class="text-[10px] uppercase tracking-widest text-white/30">Início</span>
          <span class="text-xs text-white/55 font-mono">
            {{ donkiStart(item) }}
          </span>
        </div>
      </div>
    </div>

  </div>
</template>