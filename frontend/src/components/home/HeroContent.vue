<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const visible = ref(false);

onMounted(() => {
  setTimeout(() => {
    visible.value = true;
  }, 300);
});
</script>



<template>
  <div
    class="relative z-10 w-full min-w-0 translate-y-4 opacity-0 transition-[opacity,transform] duration-[900ms] ease-out"
    :class="{ 'translate-y-0 opacity-100': visible }">
    <span class="mb-4 block text-[clamp(3rem,6vw,5rem)] font-black tracking-[0.15em] uppercase text-red-600">ASTRO</span>

    <h1
      class="mb-[1.35rem] max-w-full text-[clamp(2.4rem,5vw,3.75rem)] leading-[1.06] font-bold tracking-[-0.03em] text-balance text-white [&_em]:font-normal [&_em]:text-[red]">
      Explore o universo através dos dados da <em>NASA.</em>
    </h1>

    <p
      class="mb-8 max-w-full text-[clamp(0.9rem,1.1vw,1.05rem)] leading-[1.75] font-light text-pretty text-[rgba(232,234,240,0.58)]">
      Acompanhe imagens astronômicas, asteroides, clima espacial, missões em Marte,
      eventos naturais, exoplanetas e muito mais. Descubra informações oficiais da
      NASA por meio de uma plataforma moderna, interativa e acessível.
    </p>

    <button
      class="inline-flex items-center gap-[1.6rem][rgb(255, 37, 37)] bg-[rgb(255, 0, 0)] px-[1.6rem] py-[0.85rem] text-[0.9rem] font-medium text-white backdrop-blur-[8px] transition-[background,border-color] duration-200 hover:border-[rgb(248, 70, 70)] hover:bg-[rgb(255, 76, 76)]"
      type="button" @click="router.push('/inicio')">
      Iniciar exploração

      <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
        <path d="M3 11L11 3M11 3H5M11 3v6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
          stroke-linejoin="round" />
      </svg>
    </button>

    
  </div>
</template>
