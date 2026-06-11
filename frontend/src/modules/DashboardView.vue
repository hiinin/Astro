<script setup>
import GlobeScene from '../components/home/GlobeScene.vue'
import HeroContent from '../components/home/HeroContent.vue'
</script>

<template>
  <div class="dashboard">
    <GlobeScene />

    <!-- Layout dividido: texto esquerda | imagem direita -->
    <div class="hero-split">
      <div class="hero-left">
        <HeroContent />
      </div>
      <div class="hero-right">
        <div class="hero-right__gradient"></div>
        <img
          src="/imagens/nasa-space.jpg"
          alt="NASA Space"
          class="hero-right__img"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  position: relative;
  width: 100%;
  height: 100%;
}

.hero-split {
  position: absolute;
  inset: 0;
  z-index: 10;
  display: flex;
}

/* Lado esquerdo — conteúdo de texto */
.hero-left {
  flex: 1;
  display: flex;
  align-items: center;
  padding-left: clamp(1.5rem, 5vw, 6rem);
  padding-right: 2rem;
  max-width: 580px;
}

/* Lado direito — imagem com gradiente */
.hero-right {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.hero-right__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Gradiente que vai do escuro (esquerda) até transparente (direita) */
.hero-right__gradient {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: linear-gradient(to right, #030508 0%, #030508cc 20%, transparent 60%);
  pointer-events: none;
}
</style>
