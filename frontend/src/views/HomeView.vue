<script setup>
import AppNav from "../components/layout/AppNav.vue";

import GlobeScene from "../components/home/GlobeScene.vue";

import HeroContent from "../components/home/HeroContent.vue";
</script>


<template>
  <div class="h-screen h-dvh overflow-hidden bg-[#030508]">
    <AppNav />

    <section class="relative h-full w-full">
      <GlobeScene />

      <div
        class="absolute top-[clamp(10rem,27vh,18rem)] right-[clamp(1.5rem,8vw,12rem)] left-[clamp(1.5rem,5vw,8rem)] z-10 max-w-[580px] min-w-0"
      >
        <HeroContent />
      </div>
    </section>
  </div>
</template>

