<script setup>
import { ref } from 'vue'
import SessionForm from './components/SessionForm.vue'
import SessionList from './components/SessionList.vue'

const listRef = ref(null)

function handleCreated() {
  listRef.value?.refresh()
}
</script>

<template>
  <main>
    <h1>Pelatihan HR</h1>
    <SessionForm @created="handleCreated" />
    <SessionList ref="listRef" />
  </main>
</template>
