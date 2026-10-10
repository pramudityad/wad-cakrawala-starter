<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { deleteSession, listSessions } from '../api/sessions'

const sessions = ref([])
const status = ref('loading') // loading | data | empty | error
const errorMessage = ref('')
const search = ref('')
let controller = null

async function load() {
  controller?.abort()
  controller = new AbortController()
  status.value = 'loading'
  try {
    const data = await listSessions(search.value, controller.signal)
    sessions.value = data
    status.value = data.length ? 'data' : 'empty'
  } catch (err) {
    if (err.name === 'AbortError') return
    errorMessage.value = err.message
    status.value = 'error'
  }
}

async function handleDelete(id) {
  if (!confirm('Hapus sesi ini?')) return
  try {
    await deleteSession(id)
    await load()
  } catch (err) {
    errorMessage.value = err.message
    status.value = 'error'
  }
}

onMounted(load)
onUnmounted(() => controller?.abort())

defineExpose({ refresh: load })
</script>

<template>
  <section>
    <form class="search" @submit.prevent="load">
      <label for="search">Cari</label>
      <input id="search" v-model="search" placeholder="judul atau pemateri" />
      <button type="submit">Cari</button>
    </form>

    <p v-if="status === 'loading'">Memuat...</p>
    <p v-else-if="status === 'empty'">Tidak ada sesi.</p>
    <div v-else-if="status === 'error'" role="alert">
      <p>Gagal memuat: {{ errorMessage }}</p>
      <button type="button" @click="load">Coba lagi</button>
    </div>
    <ul v-else>
      <li v-for="s in sessions" :key="s.id">
        <span>{{ s.judul }} — {{ s.pemateri }} ({{ s.terdaftar }}/{{ s.kapasitas }})</span>
        <button type="button" @click="handleDelete(s.id)">Hapus</button>
      </li>
    </ul>
  </section>
</template>
