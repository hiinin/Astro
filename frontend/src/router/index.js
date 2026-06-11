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
        path: 'inicio',
        name: 'inicio',
        component: () => import('../modules/inicio/inicioView.vue'),
        meta: { label: 'Início' }
      },
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
      {
        path: 'foto-do-dia',
        name: 'foto-do-dia',
        component: () => import('../modules/fotododia/FotoDoDiaView.vue'),
        meta: { label: 'Foto do Dia' }
      },
      {
        path: 'camera-terra',
        name: 'camera-terra',
        component: () => import('../modules/camaraterra/CameraTeraView.vue'),
        meta: { label: 'Câmera da Terra' }
      },
      {
        path: 'clima-marte',
        name: 'clima-marte',
        component: () => import('../modules/climamarte/ClimaMarteView.vue'),
        meta: { label: 'Clima em Marte' }
      },
      {
        path: 'imagens-terra',
        name: 'imagens-terra',
        component: () => import('../modules/imagens/ImagensTerraView.vue'),
        meta: { label: 'Imagens da Terra' }
      },
      {
        path: 'rovers-marte',
        name: 'rovers-marte',
        component: () => import('../modules/roversmarte/RoversMarte.vue'),
        meta: { label: 'Rovers em Marte' }
      },
      {
        path: 'rovers-marte/:rover',
        name: 'rovers-marte-detalhe',
        component: () => import('../modules/roversmarte/RoversMarteDetalhe.vue'),
        meta: { label: 'Rovers em Marte' }
      },
      {
        path: 'clima-espacial',
        name: 'clima-espacial',
        component: () => import('../modules/climaespacial/ClimaEspacialView.vue'),
        meta: { label: 'Clima Espacial' }
      },
      {
        path: 'eventos-naturais',
        name: 'eventos-naturais',
        component: () => import('../modules/eventosnaturais/EventosNaturaisView.vue'),
        meta: { label: 'Eventos Naturais' }
      },
      {
        path: 'eventos-naturais/:id',
        name: 'eventos-naturais-detalhe',
        component: () => import('../modules/eventosnaturais/EventosNaturaisDetalhe.vue'),
        meta: { label: 'Eventos Naturais' }
      },
      {
        path: 'satelites',
        name: 'satelites',
        component: () => import('../modules/satelites/SatelitesView.vue'),
        meta: { label: 'Satélites' }
      },
      {
        path: 'sistema-solar',
        name: 'sistema-solar',
        component: () => import('../modules/sistemasolar/SistemaSolarView.vue'),
        meta: { label: 'Sistema Solar' }
      },
      {
        path: 'exoplanetas',
        name: 'exoplanetas',
        component: () => import('../modules/exoplanetas/ExoplanetasView.vue'),
        meta: { label: 'Exoplanetas' }
      },
      {
        path: 'ciencia-aberta',
        name: 'ciencia-aberta',
        component: () => import('../modules/cienciaaberta/CienciaAbertaView.vue'),
        meta: { label: 'Ciência Aberta' }
      },
      {
        path: 'midias',
        name: 'midias',
        component: () => import('../modules/midias/MidiasView.vue'),
        meta: { label: 'Mídias' }
      },
      {
        path: 'projetos',
        name: 'projetos',
        component: () => import('../modules/projetos/ProjetosView.vue'),
        meta: { label: 'Projetos' }
      },
      {
        path: 'projetos/:id',
        name: 'projetos-detalhe',
        component: () => import('../modules/projetos/ProjetosDetalhe.vue'),
        meta: { label: 'Projetos' }
      },
      {
        path: 'techtransfer',
        name: 'techtransfer',
        component: () => import('../modules/techtransfer/TechTransferView.vue'),
        meta: { label: 'TechTransfer' }
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
