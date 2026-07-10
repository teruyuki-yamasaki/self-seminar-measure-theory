<template>
  <section class="measure-diagram">
    <slot />
  </section>
</template>

<style scoped>
.measure-diagram {
  display: flex;
  min-height: 7rem;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  margin: 1.5rem 0;
  border: 1px solid var(--measure-border);
  border-radius: 0.65rem;
  background: var(--measure-panel);
  color: var(--measure-text);
  padding: 0.9rem;
  font-size: 1.3rem;
  box-shadow: var(--measure-shadow-soft);
}

:deep(p) {
  margin: 0;
}
</style>
