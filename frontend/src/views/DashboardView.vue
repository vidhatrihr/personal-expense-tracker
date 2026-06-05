<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest } from '@/utils/api.js'
import { useWhoAmI } from '@/composables/useWhoAmI.js'

const router = useRouter()
const { user, clearUser } = useWhoAmI()

const userName = ref('')
const budget = ref(0)
const budgetInput = ref(0)
const expenses = ref([])

const form = ref({ amount: '', category: '', description: '' })

// Computed totals
const totalSpent = computed(() =>
  expenses.value.reduce((sum, e) => sum + e.amount, 0)
)
const remaining = computed(() => budget.value - totalSpent.value)

// Category totals sorted descending: { Food: 120, Travel: 50 }
const breakdown = computed(() => {
  const map = {}
  for (const e of expenses.value) {
    map[e.category] = (map[e.category] || 0) + e.amount
  }
  return Object.entries(map).sort((a, b) => b[1] - a[1])
})

onMounted(async () => {
  userName.value = user.value.name

  const bRes = await apiRequest('/budget')
  const bJson = await bRes.json()
  budget.value = bJson.data.amount
  budgetInput.value = bJson.data.amount

  await loadExpenses()
})

async function loadExpenses() {
  const res = await apiRequest('/expenses')
  const json = await res.json()
  expenses.value = json.data
}

async function setBudget() {
  const res = await apiRequest('/budget', {
    method: 'POST',
    body: { amount: Number(budgetInput.value) },
  })
  const json = await res.json()
  budget.value = json.data.amount
}

async function addExpense() {
  const res = await apiRequest('/expenses', {
    method: 'POST',
    body: {
      amount: Number(form.value.amount),
      category: form.value.category,
      description: form.value.description,
    },
  })
  if (res.ok) {
    form.value = { amount: '', category: '', description: '' }
    await loadExpenses()
  }
}

async function deleteExpense(id) {
  await apiRequest(`/expenses/${id}`, { method: 'DELETE' })
  await loadExpenses()
}

async function logout() {
  await apiRequest('/logout', { method: 'POST' })
  clearUser()
  router.push('/')
}

// Format amount in INR
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

    <!-- Set budget -->
    <div class="section">
      <h2>Set Budget</h2>
      <div class="budget-form">
        <div class="form-group">
          <label for="budget-input">Monthly budget</label>
          <input id="budget-input" type="number" v-model="budgetInput" placeholder="0" min="0" />
        </div>
        <button class="btn-primary" @click="setBudget">Update</button>
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
        <button type="submit" class="btn-primary">Add</button>
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

<style scoped>
.dashboard {
  max-width: 860px;
  margin: 0 auto;
  padding: var(--gap);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--gap);
}

.dashboard-header h1 {
  font-size: 1.3rem;
  font-weight: 600;
}

.logout-btn {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border);
  font-size: 0.85rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: var(--gap);
}

.summary-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.2rem;
}

.summary-card .label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.summary-card .value {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 0.25rem;
}

.summary-card .value.accent {
  color: var(--accent);
}

.summary-card .value.danger {
  color: var(--danger);
}

.section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: var(--gap);
}

.section h2 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.budget-form {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.budget-form .form-group {
  flex: 1;
  margin-bottom: 0;
}

.budget-form .btn-primary {
  width: auto;
  white-space: nowrap;
}

.expense-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr auto;
  gap: 0.75rem;
  align-items: flex-end;
}

.expense-form-grid .form-group {
  margin-bottom: 0;
}

.expense-form-grid .btn-primary {
  width: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

thead th {
  text-align: left;
  color: var(--text-muted);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--border);
}

tbody td {
  padding: 0.65rem 0.75rem;
  border-bottom: 1px solid var(--border);
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: var(--surface-alt);
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.breakdown-item .cat-name {
  color: var(--text-muted);
}

.breakdown-item .cat-amount {
  font-weight: 500;
}

@media (max-width: 600px) {
  .expense-form-grid {
    grid-template-columns: 1fr 1fr;
  }

  .expense-form-grid .form-group:nth-child(3) {
    grid-column: 1 / -1;
  }

  .expense-form-grid .btn-primary {
    grid-column: 1 / -1;
    width: 100%;
  }
}
</style>
