<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest } from '@/utils/api.js'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

async function register() {
  error.value = ''
  const res = await apiRequest('/register', {
    method: 'POST',
    body: { name: name.value, email: email.value, password: password.value },
  })
  const json = await res.json()
  if (!res.ok) {
    error.value = json.message
    return
  }
  router.push('/dashboard')
}
</script>

<template>
  <div class="page-center">
    <div class="card">
      <h1>Create account</h1>
      <p>Get started in seconds.</p>

      <form @submit.prevent="register">
        <div class="form-group">
          <label for="name">Name</label>
          <input id="name" type="text" v-model="name" placeholder="Your name" required />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" type="email" v-model="email" placeholder="you@example.com" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <p class="error-msg" v-if="error">{{ error }}</p>

        <button type="submit" class="btn-primary">Create account</button>
      </form>

      <p class="auth-footer">
        Have an account? <RouterLink to="/">Sign in</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-footer {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-muted);
}
</style>
