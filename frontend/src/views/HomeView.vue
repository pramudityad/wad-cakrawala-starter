<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { logout } from '../api/sessions'
import { currentUser, setUser } from '../auth'
import SessionForm from '../components/SessionForm.vue'
import SessionList from '../components/SessionList.vue'

const router = useRouter()
const listRef = ref(null)

async function handleLogout() {
  await logout()
  setUser(null)
  router.push('/login')
}
</script>

<template>
  <main v-if="currentUser">
    <h1>Pelatihan HR</h1>
    <p>
      {{ currentUser.email }} ({{ currentUser.role }})
      <button type="button" @click="handleLogout">Keluar</button>
    </p>
    <SessionForm v-if="currentUser.role === 'admin'" @created="listRef?.refresh()" />
    <SessionList ref="listRef" />
  </main>
</template>
