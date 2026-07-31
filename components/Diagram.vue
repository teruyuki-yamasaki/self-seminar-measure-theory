<template>
  <section class="seminar-diagram">
    <slot />
  </section>
</template>

<style scoped>
.seminar-diagram {
  display: flex;
  min-height: 7rem;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  margin: 1.5rem 0;
  border: 1px solid var(--seminar-border);
  border-radius: 0.65rem;
  background: var(--seminar-panel);
  color: var(--seminar-text);
  padding: 0.9rem;
  font-size: 1.3rem;
  box-shadow: var(--seminar-shadow-soft);
}

:deep(p) {
  margin: 0;
}
</style>
