<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const mobileMenuOpen = ref(false)

const mainLinks = [
  { name: 'inicio', path: '/inicio', label: 'Início' },
  { name: 'foto-do-dia', path: '/foto-do-dia', label: 'Foto do Dia' },
  { name: 'asteroides', path: '/asteroides', label: 'Asteroides' },
  { name: 'camera-terra', path: '/camera-terra', label: 'Câmera da Terra' },
  { name: 'clima-marte', path: '/clima-marte', label: 'Clima em Marte' },
  { name: 'imagens-terra', path: '/imagens-terra', label: 'Imagens da Terra' },
  { name: 'rovers-marte', path: '/rovers-marte', label: 'Rovers em Marte' },
  { name: 'clima-espacial', path: '/clima-espacial', label: 'Clima Espacial' },
  { name: 'eventos-naturais', path: '/eventos-naturais', label: 'Eventos Naturais' },
  { name: 'satelites', path: '/satelites', label: 'Satélites' },
  { name: 'sistema-solar', path: '/sistema-solar', label: 'Sistema Solar' },
  { name: 'exoplanetas', path: '/exoplanetas', label: 'Exoplanetas' },
  { name: 'ciencia-aberta', path: '/ciencia-aberta', label: 'Ciência Aberta' },
  { name: 'midias', path: '/midias', label: 'Mídias' },
  { name: 'projetos', path: '/projetos', label: 'Projetos' },
  { name: 'techtransfer', path: '/techtransfer', label: 'TechTransfer' },
]

function isActive(path) {
  return route.path.startsWith(path)
}

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMenu() {
  mobileMenuOpen.value = false
}
</script>

<template>
  <header class="topbar">
    <div class="topbar-inner">
      <router-link to="/" class="topbar-logo" aria-label="Home">
        <img src="/imagens/nasa.png" alt="NASA" />
      </router-link>

      <!-- Botão hambúrguer para mobile -->
      <button
        class="mobile-toggle"
        @click="toggleMobileMenu"
        :aria-expanded="mobileMenuOpen"
        aria-label="Abrir menu de navegação"
      >
        <span class="hamburger-line" />
        <span class="hamburger-line" />
        <span class="hamburger-line" />
      </button>

      <nav :class="['topbar-nav', { open: mobileMenuOpen }]">
        <ul>
          <li v-for="link in mainLinks" :key="link.name">
            <router-link
              :to="link.path"
              :class="['nav-item', { active: isActive(link.path) }]"
              @click="closeMenu"
            >
              {{ link.label }}
            </router-link>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background-color: #1b294b;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.topbar-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 20px;
  height: 56px;
}

.topbar-logo {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  margin-right: 16px;
}

.topbar-logo img {
  height: 40px;
  width: auto;
  object-fit: contain;
}

.topbar-nav {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

.topbar-nav ul {
  display: flex;
  align-items: center;
  gap: 4px;
  list-style: none;
  margin: 0;
  padding: 0;
  white-space: nowrap;
}

.nav-item {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  color: rgba(255, 255, 255, 0.55);
  text-decoration: none;
  font-size: 13px;
  font-weight: 400;
  border-radius: 6px;
  transition: color 0.15s, background-color 0.15s;
  cursor: pointer;
}

.nav-item:hover {
  color: rgba(255, 255, 255, 0.9);
  background-color: rgba(255, 255, 255, 0.06);
}

.nav-item.active {
  color: #ffffff;
  background-color: rgba(77, 159, 255, 0.15);
  border-bottom: 2px solid #4d9fff;
}

.mobile-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  margin-left: auto;
}

.hamburger-line {
  display: block;
  width: 20px;
  height: 2px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 1px;
}

@media (max-width: 900px) {
  .mobile-toggle {
    display: flex;
  }

  .topbar-nav {
    position: absolute;
    top: 56px;
    left: 0;
    right: 0;
    background-color: #1b294b;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
  }

  .topbar-nav.open {
    max-height: 70vh;
    overflow-y: auto;
  }

  .topbar-nav ul {
    flex-direction: column;
    align-items: stretch;
    padding: 8px 0;
    gap: 0;
  }

  .nav-item {
    padding: 10px 20px;
    border-radius: 0;
  }

  .nav-item.active {
    border-bottom: none;
    border-left: 3px solid #4d9fff;
  }
}
</style>
