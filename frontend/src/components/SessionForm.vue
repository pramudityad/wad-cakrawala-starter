<script setup>
import { reactive, ref } from 'vue'
import { createSession } from '../api/sessions'

const emit = defineEmits(['created'])

const form = reactive({ judul: '', tanggal: '', pemateri: '', kapasitas: '' })
const clientError = ref('')
const serverError = ref('')
const submitting = ref(false)

function validate() {
  if (!form.judul || !form.tanggal || !form.pemateri || !form.kapasitas) {
    return 'Semua kolom wajib diisi.'
  }
  if (Number(form.kapasitas) <= 0) {
    return 'Kapasitas harus lebih dari 0.'
  }
  return ''
}

async function handleSubmit() {
  clientError.value = validate()
  if (clientError.value) return

  serverError.value = ''
  submitting.value = true
  try {
    await createSession({ ...form, kapasitas: Number(form.kapasitas), terdaftar: 0 })
    form.judul = ''
    form.tanggal = ''
    form.pemateri = ''
    form.kapasitas = ''
    emit('created')
  } catch (err) {
    serverError.value = err.message
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="judul">Judul</label>
      <input id="judul" v-model="form.judul" />
    </div>
    <div>
      <label for="tanggal">Tanggal</label>
      <input id="tanggal" v-model="form.tanggal" type="date" />
    </div>
    <div>
      <label for="pemateri">Pemateri</label>
      <input id="pemateri" v-model="form.pemateri" />
    </div>
    <div>
      <label for="kapasitas">Kapasitas</label>
      <input id="kapasitas" v-model="form.kapasitas" type="number" min="1" />
    </div>
    <p v-if="clientError" role="alert">{{ clientError }}</p>
    <p v-if="serverError" role="alert">{{ serverError }}</p>
    <button type="submit" :disabled="submitting">Tambah sesi</button>
  </form>
</template>
