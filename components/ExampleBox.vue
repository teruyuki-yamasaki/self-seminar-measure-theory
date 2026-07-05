<template>
  <aside class="my-4 rounded border border-[#cfe1df] bg-[#fbfdfc] px-4 py-3 text-[0.78rem] leading-snug">
    <p v-if="title" class="mb-2 text-[0.78rem] font-semibold text-[#176b87]">
      {{ title }}
    </p>
    <div class="example-box-content">
      <slot />
    </div>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  title?: string;
}>();
</script>

<style scoped>
:deep(p) {
  margin: 0.2rem 0;
}

:deep(.katex-display) {
  margin: 0.35rem 0;
}

:deep(.katex) {
  font-size: 0.95em;
}
</style>
