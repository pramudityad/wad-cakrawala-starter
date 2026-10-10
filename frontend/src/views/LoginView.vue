<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '../api/sessions'
import { setUser } from '../auth'

const router = useRouter()
const form = reactive({ email: '', password: '' })
const mode = ref('login') // login | register
const error = ref('')

async function submit() {
  error.value = ''
  try {
    if (mode.value === 'register') await register(form.email, form.password)
    setUser(await login(form.email, form.password))
    router.push('/')
  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <main>
    <h1>{{ mode === 'login' ? 'Masuk' : 'Daftar akun' }}</h1>
    <form @submit.prevent="submit">
      <div>
        <label for="email">Email</label>
        <input id="email" v-model="form.email" type="email" autocomplete="username" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          minlength="8"
          autocomplete="current-password"
          required
        />
      </div>
      <p v-if="error" role="alert">{{ error }}</p>
      <button type="submit">{{ mode === 'login' ? 'Masuk' : 'Daftar' }}</button>
      <button type="button" @click="mode = mode === 'login' ? 'register' : 'login'">
        {{ mode === 'login' ? 'Belum punya akun?' : 'Sudah punya akun?' }}
      </button>
    </form>
  </main>
</template>
