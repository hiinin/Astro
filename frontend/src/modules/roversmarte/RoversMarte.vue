<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const rovers = [
  {
    id: 'curiosity',
    name: 'Curiosity',
    launch: '26 Nov 2011',
    landing: '6 Ago 2012',
    status: 'Ativo',
    camera: 'MAST',
    desc: 'Explora a cratera Gale desde 2012 em busca de sinais de habitabilidade.',
  },
  {
    id: 'perseverance',
    name: 'Perseverance',
    launch: '30 Jul 2020',
    landing: '18 Fev 2021',
    status: 'Ativo',
    camera: 'MASTCAM-Z',
    desc: 'Busca sinais de vida antiga no delta do Jezero e coleta amostras.',
  },
]
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">Rovers em Marte</h1>
    </header>

    <div class="flex flex-col gap-3">
      <div
        v-for="rover in rovers"
        :key="rover.id"
        class="flex items-center gap-6 rounded-xl border border-white/[0.08] bg-white/[0.03] px-5 py-4 cursor-pointer hover:bg-white/[0.05] transition-colors"
        @click="router.push(`/rovers-marte/${rover.id}`)"
      >
        <!-- Ícone / inicial -->
        <div class="shrink-0 size-10 rounded-lg bg-white/[0.06] border border-white/[0.08] flex items-center justify-center text-sm font-bold text-white/50">
          {{ rover.name[0] }}
        </div>

        <!-- Nome + descrição -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-0.5">
            <h2 class="text-sm font-semibold">{{ rover.name }}</h2>
            <span
              class="text-[10px] font-medium px-2 py-0.5 rounded"
              :class="rover.status === 'Ativo'
                ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                : 'bg-white/5 text-white/30 border border-white/10'"
            >
              {{ rover.status }}
            </span>
          </div>
          <p class="text-xs text-white/45 truncate">{{ rover.desc }}</p>
        </div>

        <!-- Metadados -->
        <div class="shrink-0 flex items-center gap-6 text-xs">
          <div class="flex flex-col gap-0.5 text-right">
            <span class="text-[10px] uppercase tracking-widest text-white/30">Lançamento</span>
            <span class="text-white/65 font-mono">{{ rover.launch }}</span>
          </div>
          <div class="w-px h-6 bg-white/[0.08]" />
          <div class="flex flex-col gap-0.5 text-right">
            <span class="text-[10px] uppercase tracking-widest text-white/30">Pouso</span>
            <span class="text-white/65 font-mono">{{ rover.landing }}</span>
          </div>
          <div class="w-px h-6 bg-white/[0.08]" />
          <div class="flex flex-col gap-0.5 text-right">
            <span class="text-[10px] uppercase tracking-widest text-white/30">Câmera</span>
            <span class="text-white/65 font-mono">{{ rover.camera }}</span>
          </div>
        </div>

        <!-- Seta -->
        <svg class="shrink-0 text-white/20" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </div>
    </div>
  </div>
</template>