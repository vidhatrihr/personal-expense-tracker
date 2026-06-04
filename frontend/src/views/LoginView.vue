<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API = 'http://localhost:5000/api'

const email = ref('')
const password = ref('')
const error = ref('')

async function login() {
  error.value = ''
  const res = await fetch(`${API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email: email.value, password: password.value }),
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
      <h1>Sign in</h1>
      <p>Track your expenses with clarity.</p>

      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" type="email" v-model="email" placeholder="you@example.com" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <p class="error-msg" v-if="error">{{ error }}</p>

        <button type="submit" class="btn-primary">Sign in</button>
      </form>

      <p class="auth-footer">
        No account? <RouterLink to="/register">Register</RouterLink>
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
