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
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Rovers em Marte</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Rovers em Marte</h1>
      <p class="text-sm text-white/40">Fotos recentes de Curiosity e Perseverance via Nebulum Mars Rover API.</p>
    </header>

    <div class="grid grid-cols-4 gap-4">
      <div
        v-for="rover in rovers"
        :key="rover.id"
        class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 cursor-pointer hover:bg-white/[0.05] transition-colors"
        @click="router.push(`/rovers-marte/${rover.id}`)"
      >
        <div class="flex items-start justify-between mb-3">
          <h2 class="text-lg font-bold">{{ rover.name }}</h2>
          <span
            class="text-[10px] font-medium px-2 py-0.5 rounded"
            :class="rover.status === 'Ativo'
              ? 'bg-green-500/10 text-green-400 border border-green-500/20'
              : 'bg-white/5 text-white/30 border border-white/10'"
          >
            {{ rover.status }}
          </span>
        </div>
        <p class="text-xs text-white/55 leading-relaxed mb-4">{{ rover.desc }}</p>
        <dl class="grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs">
          <div>
            <span class="text-white/35">Lançamento </span>
            <span class="text-white/70">{{ rover.launch }}</span>
          </div>
          <div>
            <span class="text-white/35">Pouso </span>
            <span class="text-white/70">{{ rover.landing }}</span>
          </div>
        </dl>
      </div>
    </div>
  </div>
</template>
