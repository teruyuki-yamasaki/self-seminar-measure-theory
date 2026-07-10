<template>
  <nav class="measure-flow">
    <slot />
  </nav>
</template>

<style scoped>
.measure-flow {
  margin: 1.8rem 0;
}

:deep(ul) {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  align-items: center;
  padding: 0;
  margin: 0;
  list-style: none;
  font-size: 1.08rem;
}

:deep(li) {
  border: 1px solid var(--measure-border);
  border-radius: 999px;
  background: var(--measure-panel);
  color: var(--measure-text);
  padding: 0.45rem 0.75rem;
  box-shadow: var(--measure-shadow-soft);
}

:deep(li:not(:last-child)::after) {
  content: none;
}
</style>
