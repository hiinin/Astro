<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const rotas = [
  { name: 'asteroides', label: 'Asteroides', desc: 'Acompanhe asteroides próximos da Terra' },
  { name: 'foto-do-dia', label: 'Foto do Dia', desc: 'Imagem astronômica do dia pela NASA' },
  { name: 'camera-terra', label: 'Câmera da Terra', desc: 'Imagens da Terra capturadas do espaço' },
  { name: 'clima-marte', label: 'Clima em Marte', desc: 'Condições climáticas no planeta Marte' },
  { name: 'imagens-terra', label: 'Imagens da Terra', desc: 'Fotografias de satélite do nosso planeta' },
  { name: 'rovers-marte', label: 'Rovers em Marte', desc: 'Fotos dos rovers em missão em Marte' },
  { name: 'clima-espacial', label: 'Clima Espacial', desc: 'Atividade solar e clima no espaço' },
  { name: 'eventos-naturais', label: 'Eventos Naturais', desc: 'Eventos naturais detectados por satélites' },
  { name: 'satelites', label: 'Satélites', desc: 'Informações sobre satélites em órbita' },
  { name: 'sistema-solar', label: 'Sistema Solar', desc: 'Dados sobre planetas e corpos celestes' },
  { name: 'exoplanetas', label: 'Exoplanetas', desc: 'Planetas fora do nosso sistema solar' },
  { name: 'ciencia-aberta', label: 'Ciência Aberta', desc: 'Dados abertos de pesquisa da NASA' },
  { name: 'midias', label: 'Mídias', desc: 'Vídeos e imagens da biblioteca NASA' },
  { name: 'projetos', label: 'Projetos', desc: 'Projetos e missões da NASA' },
  { name: 'techtransfer', label: 'TechTransfer', desc: 'Transferência de tecnologia espacial' },
]
</script>

<template>
  <div class="min-h-screen px-6 py-10" style="background: radial-gradient(circle at top center, #0A1830 0%, #071426 35%, #103281 100%)">
    <div class="mx-auto max-w-7xl">
      <h1 class="mb-2 text-3xl font-bold text-white">Explorar</h1>
      <p class="mb-8 max-w-2xl text-sm leading-relaxed text-gray-400">
        A Astra reúne dados oficiais da NASA em uma plataforma moderna e acessível. 
        Navegue pelas seções abaixo para acompanhar asteroides, clima espacial, missões em Marte, 
        imagens astronômicas, exoplanetas e muito mais — tudo em tempo real, direto das APIs da NASA.
      </p>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <button
          v-for="rota in rotas"
          :key="rota.name"
          class="group flex flex-col gap-2 rounded-xl border border-white/5 bg-white/[0.02] p-5 text-left transition-all duration-200 hover:border-red-500/30 hover:bg-white/[0.05]"
          @click="router.push({ name: rota.name })"
        >
          <h2 class="text-base font-semibold text-white group-hover:text-red-400 transition-colors">
            {{ rota.label }}
          </h2>
          <p class="text-xs leading-relaxed text-gray-500">{{ rota.desc }}</p>
        </button>
      </div>
    </div>
  </div>
</template>
