<script setup>
import { ref, computed } from 'vue'
import { useRequest as useApi } from '../../composables'

const kind = ref('patent')
const query = ref('')
const { data: results, loading, error, searched, search } = useApi()

const kinds = [
  { id: 'patent', label: 'Patentes', param: 'patent', color: 'blue' },
  { id: 'software', label: 'Software', param: 'software', color: 'purple' },
  { id: 'spinoff', label: 'Spinoffs', param: 'spinoff', color: 'emerald' },
]

const activeKind = computed(() => kinds.find((k) => k.id === kind.value) ?? kinds[0])

function handleSearch() {
  const q = query.value.trim()
  if (!q) return
  const item = activeKind.value
  search(`/techtransfer/${kind.value}?${item.param}=${encodeURIComponent(q)}`, {
    transform: (data) => data.results ?? [],
  })
}

function title(row) {
  return row?.[1] ?? '—'
}

function description(row) {
  if (!Array.isArray(row)) return null
  const desc = row.find((cell, i) => i > 1 && typeof cell === 'string' && cell.length > 40)
  return desc ? desc.slice(0, 180) : null
}

function link(row) {
  return row?.find((cell) => typeof cell === 'string' && cell.startsWith('http')) ?? null
}

function cardColor() {
  const c = activeKind.value.color
  if (c === 'purple') return 'hover:border-purple-500/20 hover:shadow-purple-900/10'
  if (c === 'emerald') return 'hover:border-emerald-500/20 hover:shadow-emerald-900/10'
  return 'hover:border-blue-500/20 hover:shadow-blue-900/10'
}

function tagClass() {
  const c = activeKind.value.color
  if (c === 'purple') return 'bg-purple-500/15 text-purple-300 border-purple-500/25'
  if (c === 'emerald') return 'bg-emerald-500/15 text-emerald-300 border-emerald-500/25'
  return 'bg-blue-500/15 text-blue-300 border-blue-500/25'
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <!-- Hero Header -->
    <header class="mb-10 relative">
      <div class="absolute -top-4 -left-4 size-32 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
      <div class="relative">
        <div class="mb-4">
          <h1 class="text-3xl font-bold tracking-tight">TechTransfer</h1>
          <p class="text-sm text-white/40 mt-0.5">Patentes, software e spinoffs da NASA</p>
        </div>

        <!-- Stats bar -->
        <div class="flex items-center gap-6 mt-6 pb-6 border-b border-white/[0.06]">
          <div v-if="results?.length" class="flex items-center gap-2">
            <span class="size-2 rounded-full bg-blue-400" />
            <span class="text-xs text-white/50">{{ results.length }} resultados</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Kind Selector -->
    <div class="flex flex-wrap gap-3 mb-6">
      <button
        v-for="item in kinds"
        :key="item.id"
        type="button"
        class="group relative flex items-center gap-2.5 px-5 py-3 rounded-xl border transition-all duration-300"
        :class="kind === item.id
          ? 'bg-white/[0.06] border-white/[0.15] shadow-lg'
          : 'border-white/[0.06] hover:border-white/[0.12] hover:bg-white/[0.03]'"
        @click="kind = item.id"
      >
        <span
          class="text-sm font-medium transition-colors"
          :class="kind === item.id ? 'text-white' : 'text-white/50 group-hover:text-white/80'"
        >
          {{ item.label }}
        </span>
        <span
          v-if="kind === item.id"
          class="absolute -bottom-px left-4 right-4 h-px bg-gradient-to-r from-transparent via-purple-400/60 to-transparent"
        />
      </button>
    </div>

    <!-- Search bar -->
    <form @submit.prevent="handleSearch" class="flex gap-3 mb-10 w-full">
      <input
        v-model="query"
        :placeholder="`Buscar ${activeKind.label.toLowerCase()}...`"
        class="flex-1 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
      />
      <button
        type="submit"
        class="px-5 py-2.5 bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm rounded-lg hover:bg-blue-500/30 transition-colors"
      >
        Buscar
      </button>
    </form>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center gap-4 py-24">
      <div class="relative">
        <span class="size-10 rounded-full border-2 border-white/[0.06] border-t-purple-400 animate-spin block" />
        <span class="absolute inset-0 size-10 rounded-full border-2 border-transparent border-b-blue-400/50 animate-spin block" style="animation-duration: 1.5s" />
      </div>
      <p class="text-sm text-white/40">Buscando {{ activeKind.label.toLowerCase() }}...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="flex flex-col items-center gap-4 py-24">
      <div class="size-14 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center">
        <svg class="size-6 text-red-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
        </svg>
      </div>
      <p class="text-sm text-red-400/80">Falha ao carregar os dados ({{ error }})</p>
    </div>

    <!-- No results -->
    <div v-else-if="searched && results?.length === 0" class="flex flex-col items-center gap-4 py-20">
      <div class="size-14 rounded-full bg-white/[0.03] border border-white/[0.08] flex items-center justify-center">
        <svg class="size-6 text-white/25" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
      </div>
      <p class="text-sm text-white/40">Nenhum resultado para "<span class="text-white/60">{{ query }}</span>"</p>
    </div>

    <!-- Results Grid -->
    <div v-else-if="results?.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div
        v-for="(row, i) in results"
        :key="i"
        :class="['group relative rounded-2xl border border-white/[0.07] bg-white/[0.02] p-6 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-2xl hover:bg-white/[0.04]', cardColor()]"
      >
        <!-- Tag -->
        <div class="flex items-center justify-between mb-4">
          <span :class="['text-[10px] px-2.5 py-0.5 rounded-full border font-medium', tagClass()]">
            {{ activeKind.label }}
          </span>
          <span class="text-[10px] font-mono text-white/25">#{{ i + 1 }}</span>
        </div>

        <!-- Title -->
        <h3 class="text-sm font-semibold text-white/90 leading-snug mb-2 line-clamp-2 group-hover:text-white transition-colors">
          {{ title(row) }}
        </h3>

        <!-- Description -->
        <p v-if="description(row)" class="text-xs text-white/35 line-clamp-3 leading-relaxed mb-4">
          {{ description(row) }}
        </p>
        <div v-else class="mb-4" />

        <!-- Footer -->
        <div class="flex items-center justify-between pt-4 border-t border-white/[0.05]">
          <a
            v-if="link(row)"
            :href="link(row)"
            target="_blank"
            class="inline-flex items-center gap-1.5 text-xs text-purple-400 hover:text-purple-300 transition-colors"
            @click.stop
          >
            <svg class="size-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
            </svg>
            Ver na NASA
          </a>
          <span v-else class="text-[10px] text-white/20">—</span>
          <span class="text-[10px] text-white/20">NASA TechTransfer</span>
        </div>

        <!-- Hover arrow -->
        <div v-if="link(row)" class="absolute top-5 right-5 opacity-0 group-hover:opacity-100 transition-opacity">
          <svg class="size-4 text-white/30" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="flex flex-col items-center gap-6 py-24">
      <div class="relative">
        <div class="size-20 rounded-2xl bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-white/[0.06] flex items-center justify-center">
          <svg class="size-9 text-purple-400/60" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
          </svg>
        </div>
        <div class="absolute -top-2 -right-2 size-6 rounded-full bg-purple-500/20 border border-purple-500/30 flex items-center justify-center">
          <svg class="size-3 text-purple-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </div>
      </div>
      <div class="text-center">
        <p class="text-sm text-white/50 mb-1">Pesquise tecnologias da NASA</p>
        <p class="text-xs text-white/30">Selecione uma categoria e busque por termos como "solar", "AI", "propulsion"...</p>
      </div>
    </div>

  </div>
</template>
