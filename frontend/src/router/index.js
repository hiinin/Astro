import { createRouter, createWebHistory } from 'vue-router'
import HomeLayout from '../layouts/HomeLayout.vue'
import DefaultLayout from '../layouts/DefaultLayout.vue'

const routes = [
  {
    path: '/',
    component: HomeLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('../modules/DashboardView.vue')
      }
    ]
  },
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: 'asteroides',
        name: 'asteroides',
        component: () => import('../modules/asteroides/AsteroidesView.vue'),
        meta: { label: 'Asteroides' }
      },
      {
        path: 'asteroides/:id',
        name: 'asteroides-detail',
        component: () => import('../modules/asteroides/AsteroidesDetailView.vue'),
        meta: { label: 'Asteroides' }
      },

      // TODO: Missões
      // { path: 'missoes', name: 'missoes', component: () => import('../views/MissoesView.vue') },

      // TODO: Ciência Aberta (OSDR)
      // { path: 'ciencia-aberta', name: 'ciencia-aberta', component: () => import('../views/CienciaAbertaView.vue') },

      // TODO: Imagem do Dia (APOD)
      // { path: 'imagem-do-dia', name: 'imagem-do-dia', component: () => import('../views/ImagemDiaView.vue') },

      // TODO: Imagens da Terra (EPIC)
      // { path: 'imagens-da-terra', name: 'imagens-da-terra', component: () => import('../views/ImagensTerraView.vue') },

      // TODO: Mars Rover
      // { path: 'mars-rover', name: 'mars-rover', component: () => import('../views/MarsRoverView.vue') },

      // TODO: Veículos Espaciais
      // { path: 'veiculos-espaciais', name: 'veiculos-espaciais', component: () => import('../views/VeiculosEspaciaisView.vue') },

      // TODO: Equipamentos
      // { path: 'equipamentos', name: 'equipamentos', component: () => import('../views/EquipamentosView.vue') },

      // TODO: Sujeitos de Pesquisa
      // { path: 'sujeitos-de-pesquisa', name: 'sujeitos-de-pesquisa', component: () => import('../views/SujeitosPesquisaView.vue') },

      // TODO: Amostras Biológicas
      // { path: 'amostras-biologicas', name: 'amostras-biologicas', component: () => import('../views/AmostrasBiologicasView.vue') },

      // TODO: Favoritos
      // { path: 'favoritos', name: 'favoritos', component: () => import('../views/FavoritosView.vue') },

      // TODO: Sobre a API
      // { path: 'sobre-a-api', name: 'sobre-a-api', component: () => import('../views/SobreAPIView.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
