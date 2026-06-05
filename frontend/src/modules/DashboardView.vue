<script setup>
import GlobeScene from '../components/home/GlobeScene.vue'
import HeroContent from '../components/home/HeroContent.vue'
</script>

<template>
  <div class="dashboard">
    <GlobeScene />
    <div class="hero-wrapper">
      <HeroContent />
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  position: relative;
  width: 100%;
  height: 100%;
}

.hero-wrapper {
  position: absolute;
  top: clamp(8rem, 22vh, 14rem);
  right: clamp(1.5rem, 8vw, 10rem);
  left: clamp(1.5rem, 5vw, 6rem);
  z-index: 10;
  max-width: 580px;
}
</style>
