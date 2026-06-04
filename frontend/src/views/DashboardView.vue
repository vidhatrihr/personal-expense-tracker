<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// user & state
const userName = ref('')
const budget = ref(0)
const budgetInput = ref(0)
const expenses = ref([])

// new expense form
const form = ref({ amount: '', category: '', description: '' })

const API = 'http://localhost:5000/api'
const opts = { credentials: 'include' }

// --- summary computed ---
const totalSpent = computed(() =>
  expenses.value.reduce((sum, e) => sum + e.amount, 0)
)
const remaining = computed(() => budget.value - totalSpent.value)

// category breakdown: { Food: 120, Travel: 50, ... }
const breakdown = computed(() => {
  const map = {}
  for (const e of expenses.value) {
    map[e.category] = (map[e.category] || 0) + e.amount
  }
  return Object.entries(map).sort((a, b) => b[1] - a[1])
})

// --- fetch on mount ---
onMounted(async () => {
  // verify session, get user info
  const meRes = await fetch(`${API}/whoami`, opts)
  if (!meRes.ok) { router.push('/'); return }
  const me = await meRes.json()
  userName.value = me.data.name

  // load budget
  const bRes = await fetch(`${API}/budget`, opts)
  const bJson = await bRes.json()
  budget.value = bJson.data.amount
  budgetInput.value = bJson.data.amount

  // load expenses
  await loadExpenses()
})

async function loadExpenses() {
  const res = await fetch(`${API}/expenses`, opts)
  const json = await res.json()
  expenses.value = json.data
}

async function setBudget() {
  const res = await fetch(`${API}/budget`, {
    ...opts,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount: Number(budgetInput.value) }),
  })
  const json = await res.json()
  budget.value = json.data.amount
}

async function addExpense() {
  const res = await fetch(`${API}/expenses`, {
    ...opts,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: Number(form.value.amount),
      category: form.value.category,
      description: form.value.description,
    }),
  })
  if (res.ok) {
    form.value = { amount: '', category: '', description: '' }
    await loadExpenses()
  }
}

async function deleteExpense(id) {
  await fetch(`${API}/expenses/${id}`, { ...opts, method: 'DELETE' })
  await loadExpenses()
}

async function logout() {
  await fetch(`${API}/logout`, { ...opts, method: 'POST' })
  router.push('/')
}

// currency formatter
function fmt(n) {
  return '₹' + Number(n).toFixed(2)
}
</script>

<template>
  <div class="dashboard">

    <!-- Header -->
    <div class="dashboard-header">
      <h1>Hey, {{ userName }} 👋</h1>
      <button class="logout-btn" @click="logout">Sign out</button>
    </div>

    <!-- Summary cards -->
    <div class="summary-grid">
      <div class="summary-card">
        <div class="label">Budget</div>
        <div class="value">{{ fmt(budget) }}</div>
      </div>
      <div class="summary-card">
        <div class="label">Spent</div>
        <div class="value danger">{{ fmt(totalSpent) }}</div>
      </div>
      <div class="summary-card">
        <div class="label">Remaining</div>
        <div class="value" :class="remaining >= 0 ? 'accent' : 'danger'">{{ fmt(remaining) }}</div>
      </div>
    </div>

    <!-- Budget -->
    <div class="section">
      <h2>Set Budget</h2>
      <div class="budget-form">
        <div class="form-group">
          <label for="budget-input">Monthly budget</label>
          <input id="budget-input" type="number" v-model="budgetInput" placeholder="0" min="0" />
        </div>
        <button class="btn-primary" style="width: auto" @click="setBudget">Update</button>
      </div>
    </div>

    <!-- Add expense -->
    <div class="section">
      <h2>Add Expense</h2>
      <form @submit.prevent="addExpense" class="expense-form-grid">
        <div class="form-group">
          <label for="exp-amount">Amount</label>
          <input id="exp-amount" type="number" v-model="form.amount" placeholder="0" min="0" required />
        </div>
        <div class="form-group">
          <label for="exp-category">Category</label>
          <input id="exp-category" type="text" v-model="form.category" placeholder="Food, Travel…" required />
        </div>
        <div class="form-group">
          <label for="exp-desc">Description</label>
          <input id="exp-desc" type="text" v-model="form.description" placeholder="What was it for?" />
        </div>
        <button type="submit" class="btn-primary" style="width: auto">Add</button>
      </form>
    </div>

    <!-- Category breakdown -->
    <div class="section" v-if="breakdown.length">
      <h2>By Category</h2>
      <div class="breakdown-list">
        <div class="breakdown-item" v-for="[cat, amt] in breakdown" :key="cat">
          <span class="cat-name">{{ cat }}</span>
          <span class="cat-amount">{{ fmt(amt) }}</span>
        </div>
      </div>
    </div>

    <!-- Expenses table -->
    <div class="section">
      <h2>All Expenses</h2>
      <div class="empty" v-if="!expenses.length">No expenses yet.</div>
      <table v-else>
        <thead>
          <tr>
            <th>Category</th>
            <th>Description</th>
            <th>Amount</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="expense in expenses" :key="expense.id">
            <td>{{ expense.category }}</td>
            <td>{{ expense.description }}</td>
            <td>{{ fmt(expense.amount) }}</td>
            <td>
              <button class="btn-danger" @click="deleteExpense(expense.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>
