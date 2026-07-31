<template>
  <nav class="seminar-flow">
    <slot />
  </nav>
</template>

<style scoped>
.seminar-flow {
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
  border: 1px solid var(--seminar-border);
  border-radius: 999px;
  background: var(--seminar-panel);
  color: var(--seminar-text);
  padding: 0.45rem 0.75rem;
  box-shadow: var(--seminar-shadow-soft);
}

:deep(li:not(:last-child)::after) {
  content: none;
}
</style>
