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
    <p
      class="mb-5 max-w-full font-['JetBrains_Mono',monospace] text-[0.72rem] tracking-[0.22em] text-balance text-[#4db2ff] uppercase">
      Exploramos o desconhecido
    </p>

    <h1
      class="mb-[1.35rem] max-w-full text-[clamp(2.4rem,5vw,3.75rem)] leading-[1.06] font-bold tracking-[-0.03em] text-balance text-white [&_em]:font-normal [&_em]:text-[#4db2ff]">
      Para o benefício de toda a <em>humanidade.</em>
    </h1>

    <p
      class="mb-8 max-w-full text-[clamp(0.9rem,1.1vw,1.05rem)] leading-[1.75] font-light text-pretty text-[rgba(232,234,240,0.58)]">
      A NASA explora o desconhecido em ar, espaço e tecnologia, conduzindo
      pesquisa e desenvolvendo novas tecnologias para o benefício de toda a
      humanidade.
    </p>

    <button
      class="inline-flex items-center gap-[0.6rem] rounded-full border border-[rgba(255,255,255,0.18)] bg-[rgba(255,255,255,0.04)] px-[1.6rem] py-[0.85rem] text-[0.9rem] font-medium text-white backdrop-blur-[8px] transition-[background,border-color] duration-200 hover:border-[rgba(77,178,255,0.45)] hover:bg-[rgba(77,178,255,0.12)]"
      type="button" @click="router.push('/asteroides')">
      Explorar Asteroides

      <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
        <path d="M3 11L11 3M11 3H5M11 3v6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
          stroke-linejoin="round" />
      </svg>
    </button>
  </div>
</template>
