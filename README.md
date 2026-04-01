# Expense Tracker — Project Report

**Stack:** Flask (Python) · SQLite · Vue 3 (Vite) · Pure CSS  
**Demo credentials:** `vidhatri@example.com` / `password123`

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Structure](#2-project-structure)
3. [Backend](#3-backend)
   - 3.1 [Dependencies](#31-dependencies)
   - 3.2 [app.py — Entry Point](#32-apppy--entry-point)
   - 3.3 [models.py — Database Models](#33-modelspy--database-models)
   - 3.4 [populate_db.py — Seed Data](#34-populate_dbpy--seed-data)
   - 3.5 [routes/auth.py — Auth Blueprint](#35-routesauthpy--auth-blueprint)
   - 3.6 [routes/expenses.py — Expenses Blueprint](#36-routesexpensespy--expenses-blueprint)
4. [Frontend](#4-frontend)
   - 4.1 [index.html](#41-indexhtml)
   - 4.2 [main.js](#42-mainjs)
   - 4.3 [App.vue](#43-appvue)
   - 4.4 [router/index.js — Client-Side Routing](#44-routerindexjs--client-side-routing)
   - 4.5 [style.css — Global Styles](#45-stylecss--global-styles)
   - 4.6 [LoginView.vue](#46-loginviewvue)
   - 4.7 [RegisterView.vue](#47-registerviewvue)
   - 4.8 [DashboardView.vue](#48-dashboardviewvue)
5. [Business Logic & Data Flow](#5-business-logic--data-flow)
6. [API Reference](#6-api-reference)
7. [Running the Application](#7-running-the-application)

---

## 1. Project Overview

The Expense Tracker is a web application where a user can:

- Create an account and log in
- Set a monthly budget
- Submit expenses with an amount, category, and description
- View a summary of total spent and remaining budget
- See a breakdown of spending by category
- Delete individual expenses

Each user's data is private — budgets and expenses are tied to the logged-in user.

---

## 2. Project Structure

```
expense-tracker-app/
├── AGENTS.md                        # architecture and coding guidelines
├── backend/
│   ├── app.py                       # Flask app — config, db, blueprints
│   ├── models.py                    # database tables as Python classes
│   ├── populate_db.py               # seed function — demo data
│   ├── requirements.txt             # pip packages
│   ├── expense_tracker.db           # SQLite database (auto-created)
│   └── routes/
│       ├── __init__.py              # makes routes/ a Python package
│       ├── auth.py                  # register, login, logout, me
│       └── expenses.py              # budget and expense endpoints
└── frontend/
    ├── index.html                   # HTML shell
    └── src/
        ├── main.js                  # creates Vue app, mounts it
        ├── style.css                # all CSS — global and component styles
        ├── App.vue                  # root Vue component
        ├── router/
        │   └── index.js             # URL → component mapping
        └── views/
            ├── LoginView.vue        # /  — login page
            ├── RegisterView.vue     # /register — signup page
            └── DashboardView.vue    # /dashboard — main app
```

---

## 3. Backend

The backend is a Flask web server that exposes a REST API. It runs on port **5000**. The frontend communicates with it exclusively via HTTP requests.

### 3.1 Dependencies

Defined in `requirements.txt`:

| Package | Purpose |
| --- | --- |
| `flask` | Web framework — handles HTTP routing |
| `flask-cors` | Allows the frontend (port 5173) to call the backend (port 5000) |
| `flask-login` | Manages user sessions — tracks who is logged in |
| `flask-sqlalchemy` | ORM — lets us write Python classes instead of raw SQL |
| `werkzeug` | Bundled with Flask — used for password hashing |

Install with: `pip install -r requirements.txt`

---

### 3.2 `app.py` — Entry Point

This is the first file Flask runs. It wires everything together.

**What it does, step by step:**

1. **Creates the Flask app** and sets a `secret_key`. The secret key is used to sign session cookies — without it, sessions don't work.

2. **Configures session cookies** for cross-site requests:
   - `SESSION_COOKIE_SAMESITE="None"` — allows the cookie to be sent from a different origin (the Vite dev server at port 5173)
   - `SESSION_COOKIE_SECURE=True` — cookie is only sent over HTTPS
   - `SESSION_COOKIE_HTTPONLY=True` — JavaScript in the browser cannot read the cookie (security measure)

3. **Sets the database URI** to `sqlite:///expense_tracker.db`. SQLite creates this file automatically inside the `backend/` folder on first run.

4. **Configures CORS** with `supports_credentials=True` and restricts it to `http://localhost:5173`. This is required because the browser blocks cross-origin requests with cookies by default.

5. **Initialises Flask-SQLAlchemy** by calling `db.init_app(app)`. This connects the `db` object from `models.py` to this specific Flask app.

6. **Configures Flask-Login** with a `LoginManager`. The `load_user` function is called by Flask-Login on every request to load the currently logged-in user from the database using their ID stored in the session cookie.

7. **Registers blueprints** under the `/api` URL prefix. All API URLs will start with `/api/`.

8. **Inside `app_context()`**: Creates all database tables (if they don't exist yet), then calls `seed_db()` to insert demo data on a fresh database.

9. **Starts the server** on port 5000 in debug mode (auto-reloads on code changes).

---

### 3.3 `models.py` — Database Models

Each class here represents one table in the SQLite database. Flask-SQLAlchemy translates these Python classes into SQL `CREATE TABLE` statements.

**`db = SQLAlchemy()`**  
Creates the database object. It is initialised inside `app.py` with `db.init_app(app)`.

#### `User` table (`users`)

| Column | Type | Details |
| --- | --- | --- |
| `id` | Integer | Primary key, auto-incremented |
| `name` | String | User's display name |
| `email` | String | Unique — no two users share an email |
| `password` | String | Stores a **hashed** password, never plain text |

`UserMixin` is inherited from Flask-Login. It provides default implementations for methods Flask-Login needs (e.g. `is_authenticated`, `get_id`).

**Relationships on `User`:**
- `budget` — links to one `Budget` row (`uselist=False` means it's a single object, not a list)
- `expenses` — links to many `Expense` rows (a list)

#### `Budget` table (`budgets`)

| Column | Type | Details |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `amount` | Float | The budget amount in ₹ |
| `user_id` | Integer | Foreign key → `users.id` |

Each user has at most one budget row.

#### `Expense` table (`expenses`)

| Column | Type | Details |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `amount` | Float | How much was spent |
| `category` | String | e.g. Food, Transport, Shopping |
| `description` | String | Free-text note |
| `user_id` | Integer | Foreign key → `users.id` |

A user can have many expense rows.

**How relationships work:**  
`back_populates` connects the two sides of a relationship. For example, `User.expenses` and `Expense.user` point to each other. Accessing `current_user.expenses` runs a SQL query automatically and returns a list of that user's expense objects.

---

### 3.4 `populate_db.py` — Seed Data

Defines a single function: `seed_db()`. It is imported and called in `app.py` every time the server starts.

**Safety check — the first line inside the function:**
```python
if User.query.count() > 0:
    return
```
This counts how many users exist. If the count is greater than zero, the database already has data — so the function returns immediately without doing anything. This prevents duplicate data from being inserted on every restart.

**What it seeds (on a fresh database):**

1. Creates a user named **Vidhatri** with email `vidhatri@example.com` and a hashed password.
2. Calls `db.session.flush()` — this sends the INSERT to the database without committing, which gives the user an `id` so it can be used as a foreign key in the next inserts.
3. Creates a `Budget` of ₹50,000 linked to that user.
4. Creates 5 sample `Expense` rows across different categories: Food, Transport, Shopping, Utilities.
5. Calls `db.session.commit()` to permanently save everything.

---

### 3.5 `routes/auth.py` — Auth Blueprint

A **Blueprint** is Flask's way of grouping related routes into a separate file. This blueprint is imported and registered in `app.py` with the prefix `/api`, so all URLs here become `/api/register`, `/api/login`, etc.

---

#### `POST /api/register`

**Purpose:** Create a new user account.

**Request body (JSON):**
```json
{ "name": "Alice", "email": "alice@example.com", "password": "secret" }
```

**Logic:**
1. Extract `name`, `email`, `password` from the request JSON.
2. Query the database for any existing user with that email. If one exists, return a `400` error with the message `"Email already registered"`.
3. Create a new `User` object. The password is passed through `generate_password_hash()` — this converts the plain text password into a long, irreversible hash string before saving. Example output: `pbkdf2:sha256:600000$...`
4. Add the user to the session and commit (save to database).
5. Call `login_user(user)` — this writes the user's ID into the session cookie so they are considered logged in immediately.
6. Return `200` with a success message.

---

#### `POST /api/login`

**Purpose:** Log in an existing user.

**Request body (JSON):**
```json
{ "email": "alice@example.com", "password": "secret" }
```

**Logic:**
1. Extract `email` and `password`.
2. Query the database for a user with that email. Note: we query **only by email**, not by password — this is important.
3. If no user found, or if `check_password_hash(user.password, password)` returns `False`, return `401` with `"Invalid credentials"`. `check_password_hash` takes the stored hash and the plain text input and returns `True` only if they match.
4. Call `login_user(user)` to establish the session.
5. Return `200` with the user's name and email.

---

#### `POST /api/logout`

**Purpose:** Log out the current user.

**Requires:** Active session (`@login_required`). If no session, Flask-Login returns `401`.

**Logic:** Calls `logout_user()`, which clears the session cookie. Returns `200`.

---

#### `GET /api/me`

**Purpose:** Return the currently logged-in user's info. Used by the dashboard on mount to verify the session is still valid.

**Requires:** Active session (`@login_required`).

**Logic:** `current_user` is a proxy object provided by Flask-Login that always points to the logged-in user. Returns their `name` and `email`.

**Response:**
```json
{ "data": { "name": "Vidhatri", "email": "vidhatri@example.com" } }
```

---

### 3.6 `routes/expenses.py` — Expenses Blueprint

All routes here require `@login_required`. `current_user` is always the logged-in user.

---

#### `GET /api/budget`

**Purpose:** Return the current user's budget amount.

**Logic:**  
Access `current_user.budget` — SQLAlchemy automatically queries the `budgets` table filtered by `user_id`. If no budget row exists yet, return `0`. Otherwise return the `amount`.

**Response:**
```json
{ "data": { "amount": 50000.0 } }
```

---

#### `POST /api/budget`

**Purpose:** Set or update the budget amount.

**Request body:** `{ "amount": 50000 }`

**Logic (upsert pattern):**
1. Check if `current_user.budget` exists.
2. If it doesn't exist → create a new `Budget` row and add it to the session.
3. If it does exist → update the `.amount` field on the existing row.
4. Commit. SQLAlchemy tracks which objects were changed and generates the correct SQL (`INSERT` or `UPDATE`).

**Response:**
```json
{ "message": "Budget updated", "data": { "amount": 50000.0 } }
```

---

#### `GET /api/expenses`

**Purpose:** Return all expenses for the current user.

**Logic:**  
`current_user.expenses` returns a list of `Expense` objects for that user. Convert each to a plain dictionary (Python objects can't be serialised to JSON directly). Return the list.

**Response:**
```json
{
  "data": [
    { "id": 1, "amount": 1200.0, "category": "Food", "description": "Grocery run" },
    ...
  ]
}
```

---

#### `POST /api/expenses`

**Purpose:** Add a new expense.

**Request body:** `{ "amount": 500, "category": "Transport", "description": "Uber to office" }`

**Logic:**  
Create an `Expense` object with the provided fields and `user_id=current_user.id`. Add and commit. Return the saved expense (including its auto-generated `id`).

---

#### `DELETE /api/expenses/<expense_id>`

**Purpose:** Delete a specific expense by its ID.

**Logic:**  
`expense_id` is a URL path variable (e.g. `/api/expenses/3` passes `3`). Query the expense by that ID, delete it from the session, commit. Return a success message.

---

## 4. Frontend

The frontend is a Vue 3 Single Page Application (SPA). The browser loads the app once, and Vue Router handles navigation between pages without full page reloads. It runs on port **5173**.

### 4.1 `index.html`

The single HTML file that the browser loads. It contains:
- `<meta charset="UTF-8">` — character encoding
- `<meta name="viewport">` — enables correct scaling on mobile
- `<meta name="description">` — SEO description for search engines
- `<title>Expense Tracker</title>` — browser tab title
- Two `<link>` tags to load the **Inter** font from Google Fonts
- `<div id="app"></div>` — empty container where Vue injects the entire interface
- `<script type="module" src="/src/main.js">` — loads the Vue app

---

### 4.2 `main.js`

The JavaScript entry point.

```js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './style.css';

const app = createApp(App);
app.use(router);
app.mount('#app');
```

- `createApp(App)` — creates the Vue application using `App.vue` as the root component
- `app.use(router)` — installs Vue Router so all components can use `<RouterLink>` and `useRouter()`
- `import './style.css'` — loads all global styles once
- `app.mount('#app')` — attaches the Vue app to the `<div id="app">` in `index.html`

---

### 4.3 `App.vue`

```vue
<script setup></script>

<template>
  <RouterView />
</template>
```

This is the root component. It contains only `<RouterView />`, which is a placeholder that Vue Router replaces with the correct view component based on the current URL. There is no logic here — it is intentionally kept as thin as possible.

---

### 4.4 `router/index.js` — Client-Side Routing

Defines which Vue component to render for each URL.

```js
routes: [
  { path: '/',          component: LoginView },
  { path: '/register',  component: RegisterView },
  { path: '/dashboard', component: DashboardView },
]
```

`createWebHistory` uses the browser's History API for clean URLs (no `#` in the URL). When the user navigates to `/dashboard`, Vue Router swaps `<RouterView />` to render `DashboardView.vue` — no page reload happens.

---

### 4.5 `style.css` — Global Styles

All CSS lives in this single file. No CSS framework is used.

#### Design Tokens (CSS Variables)

Defined on `:root` so they are available everywhere:

| Variable | Value | Usage |
| --- | --- | --- |
| `--bg` | `#0f0f11` | Page background |
| `--surface` | `#18181c` | Cards and section backgrounds |
| `--surface-alt` | `#222228` | Input backgrounds, table row hover |
| `--border` | `#2e2e36` | All borders |
| `--accent` | `#c8f55a` | Primary action color (lime-green) |
| `--text` | `#e8e8ee` | Main text |
| `--text-muted` | `#7a7a8c` | Labels, secondary text |
| `--danger` | `#f55a5a` | Errors, delete buttons, overspend |
| `--radius` | `10px` | Border radius for cards |
| `--gap` | `1.5rem` | Standard spacing between sections |

Variables are named by **context**, not by color — e.g. `--danger` not `--red`. This makes it easy to change the color scheme without renaming variables.

#### Key Style Classes

| Class | What it styles |
| --- | --- |
| `.page-center` | Full-screen flexbox centering — used by login and register pages |
| `.card` | White-bordered dark box — wraps auth forms |
| `.form-group` | Label + input stacked vertically |
| `.btn-primary` | Accent-colored full-width button |
| `.btn-danger` | Outlined red button — used for Delete |
| `.error-msg` | Red inline error text below forms |
| `.dashboard` | Max-width centered container for dashboard content |
| `.dashboard-header` | Flexbox row — username on left, sign out on right |
| `.summary-grid` | CSS Grid — auto-fills summary cards side by side |
| `.summary-card` | Individual stat card (Budget, Spent, Remaining) |
| `.section` | Dark bordered box — wraps each dashboard section |
| `.budget-form` | Flex row — input and button side by side |
| `.expense-form-grid` | CSS Grid `1fr 1fr 2fr auto` — 4-column expense form |
| `.breakdown-list` | Vertical list of category rows |
| `.empty` | Centered muted text — shown when no expenses exist |

#### Responsive Behavior

At screen widths below **600px**, the 4-column expense form collapses:
- Amount and Category share the first row
- Description spans full width
- Add button spans full width

---

### 4.6 `LoginView.vue`

**Route:** `/`

#### State (reactive variables)
| Variable | Type | Purpose |
| --- | --- | --- |
| `email` | `ref('')` | Bound to email input |
| `password` | `ref('')` | Bound to password input |
| `error` | `ref('')` | Holds error message to display |

#### `login()` function

1. Clears any previous error.
2. Sends `POST /api/login` with email and password as JSON. `credentials: 'include'` is required so the browser sends and receives session cookies across origins.
3. Parses the response JSON.
4. If the response status is not OK (e.g. `401`), sets `error.value` to the message from the server — this renders under the form.
5. If successful, calls `router.push('/dashboard')` to navigate to the dashboard.

#### Template

- A `.page-center` div centers the card on screen.
- A `.card` contains the heading, subtext, and form.
- The form has `@submit.prevent="login"` — `prevent` stops the browser's default form submission (page reload); instead it calls the `login()` function.
- Each input uses `v-model` — this is Vue's two-way binding. When the user types, `email.value` updates automatically.
- `v-if="error"` — the error paragraph is only rendered when `error` has content.
- A `<RouterLink to="/register">` renders as an `<a>` tag that navigates without a page reload.

---

### 4.7 `RegisterView.vue`

**Route:** `/register`

#### State
| Variable | Type | Purpose |
| --- | --- | --- |
| `name` | `ref('')` | Bound to name input |
| `email` | `ref('')` | Bound to email input |
| `password` | `ref('')` | Bound to password input |
| `error` | `ref('')` | Holds error message to display |

#### `register()` function

1. Clears any previous error.
2. Sends `POST /api/register` with name, email, password as JSON.
3. If the response is not OK (e.g. email already taken), shows the error message inline.
4. If successful (the backend has already logged the user in — session cookie is set), redirects to `/dashboard`.

The user never sees the login page after registering — they go straight to the dashboard.

#### Template

Same card layout as Login. Has an extra Name input field. The submit button says "Create account". A link at the bottom navigates back to `/` for users who already have an account.

---

### 4.8 `DashboardView.vue`

**Route:** `/dashboard`

This is the main application screen. It loads all data on mount and provides forms to interact with it.

#### State
| Variable | Type | Purpose |
| --- | --- | --- |
| `userName` | `ref('')` | Displays in the header greeting |
| `budget` | `ref(0)` | The saved budget amount (from API) |
| `budgetInput` | `ref(0)` | Bound to the budget input field |
| `expenses` | `ref([])` | List of all expense objects |
| `form` | `ref({...})` | Holds the new expense form fields |
| `API` | constant | Base URL `http://localhost:5000/api` |
| `opts` | constant | `{ credentials: 'include' }` — reused in all fetch calls |

#### Computed Properties

**`totalSpent`**  
Uses `Array.reduce()` to sum all `expense.amount` values. Recalculates automatically whenever `expenses` changes.

**`remaining`**  
`budget - totalSpent`. Recalculates when either changes.

**`breakdown`**  
Iterates through all expenses and groups amounts by category into a plain object (e.g. `{ Food: 2000, Transport: 500 }`). Then converts to an array of `[category, total]` pairs and sorts by total descending (highest spend first). Recalculates when `expenses` changes.

#### `onMounted()` — Data Loading

Runs once when the component is first rendered. Performs three sequential API calls:

1. **`GET /api/me`** — Verifies the session is still valid. If the response is not OK (401 — session expired or not logged in), immediately redirects to `/`. If OK, sets `userName` from the response.
2. **`GET /api/budget`** — Loads the budget amount. Sets both `budget` (displayed in summary) and `budgetInput` (pre-fills the input field).
3. **`loadExpenses()`** — Loads all expenses.

This pattern ensures unauthenticated users cannot view the dashboard.

#### Functions

**`loadExpenses()`**  
Fetches `GET /api/expenses` and sets `expenses.value` to the returned array. Called on mount and after every add or delete.

**`setBudget()`**  
Sends `POST /api/budget` with `budgetInput.value` converted to a number. Updates `budget.value` from the response so the summary cards update instantly.

**`addExpense()`**  
Sends `POST /api/expenses` with the form fields. On success: clears the form (resets all fields to empty strings), then calls `loadExpenses()` to refresh the table. The new expense immediately appears in the table, totals, and category breakdown.

**`deleteExpense(id)`**  
Sends `DELETE /api/expenses/{id}`. Then calls `loadExpenses()` to refresh. The deleted expense disappears from the table and all computed values update.

**`logout()`**  
Sends `POST /api/logout`. Then navigates to `/`. The session cookie is cleared server-side.

**`fmt(n)`**  
A helper function. Takes a number and returns a formatted string: `₹` + the number rounded to 2 decimal places. Used everywhere an amount is displayed.

#### Template Structure

```
<div class="dashboard">
  ├── .dashboard-header          ← "Hey, Vidhatri 👋" + Sign out button
  ├── .summary-grid              ← Budget | Spent | Remaining cards
  ├── .section (Set Budget)      ← Number input + Update button
  ├── .section (Add Expense)     ← Amount + Category + Description + Add
  ├── .section (By Category)     ← v-if only shown when expenses exist
  └── .section (All Expenses)    ← Table with delete buttons, or empty state
```

**Summary cards — color logic:**  
The Remaining card's value text uses `:class="remaining >= 0 ? 'accent' : 'danger'"`. This Vue binding applies the `.accent` class (lime-green) when the user is within budget, and `.danger` (red) when they've overspent.

**Category breakdown — `v-if`:**  
The entire "By Category" section is wrapped in `v-if="breakdown.length"`. It only renders when there is at least one expense. When the expense list is empty, this section disappears entirely.

**Expenses table — `v-if` / `v-else`:**  
If `expenses.length` is zero, a `.empty` paragraph renders ("No expenses yet."). Otherwise, the table renders. `v-for="expense in expenses"` iterates the array and renders one `<tr>` per expense. `:key="expense.id"` tells Vue to track each row by its unique ID for efficient DOM updates.

---

## 5. Business Logic & Data Flow

### Registration Flow

```
User fills form → POST /api/register
  → Server creates User (hashed password)
  → Server calls login_user() — session cookie set
  → 200 OK
  → Frontend redirects to /dashboard
```

### Login Flow

```
User fills form → POST /api/login
  → Server finds user by email
  → check_password_hash() verifies password
  → login_user() — session cookie set
  → 200 OK
  → Frontend redirects to /dashboard
```

### Dashboard Load Flow

```
Vue mounts DashboardView
  → GET /api/me (verify session)
      → 401: redirect to /
      → 200: set userName
  → GET /api/budget → set budget + budgetInput
  → GET /api/expenses → set expenses array
  → computed values (totalSpent, remaining, breakdown) calculate automatically
  → template renders with all data
```

### Add Expense Flow

```
User fills form → click Add → addExpense()
  → POST /api/expenses (amount, category, description)
  → Server creates Expense linked to current_user.id
  → 200 OK
  → Frontend clears form
  → loadExpenses() → GET /api/expenses
  → expenses array updates → computed values recalculate → UI refreshes
```

### Delete Expense Flow

```
User clicks Delete → deleteExpense(id)
  → DELETE /api/expenses/{id}
  → Server deletes the row
  → 200 OK
  → loadExpenses() → GET /api/expenses
  → expenses array updates → UI refreshes
```

### Session Persistence

The browser stores the session as a cookie. On every API call, `credentials: 'include'` ensures the cookie is sent automatically. Flask-Login reads the cookie, looks up the user ID in the session, and calls `load_user()` to fetch the full User object from the database — making it available as `current_user` in any route.

### Password Security

Passwords are never stored as plain text. `generate_password_hash('password123')` produces something like:
```
pbkdf2:sha256:600000$Xk3...xyz...abc
```
This string encodes the algorithm, number of iterations, salt, and hash. `check_password_hash(stored_hash, 'password123')` re-runs the same algorithm and compares — returning `True` only on a match. Even if the database is leaked, the passwords cannot be reversed.

---

## 6. API Reference

All endpoints are prefixed with `/api`. All responses are JSON with the shape `{ "data": ..., "message": "..." }`.

| Method | URL | Auth | Request Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/api/register` | No | `{ name, email, password }` | `{ message }` |
| `POST` | `/api/login` | No | `{ email, password }` | `{ message, data: { name, email } }` |
| `POST` | `/api/logout` | Yes | — | `{ message }` |
| `GET` | `/api/me` | Yes | — | `{ data: { name, email } }` |
| `GET` | `/api/budget` | Yes | — | `{ data: { amount } }` |
| `POST` | `/api/budget` | Yes | `{ amount }` | `{ message, data: { amount } }` |
| `GET` | `/api/expenses` | Yes | — | `{ data: [ ...expenses ] }` |
| `POST` | `/api/expenses` | Yes | `{ amount, category, description }` | `{ message, data: expense }` |
| `DELETE` | `/api/expenses/<id>` | Yes | — | `{ message }` |

**Auth = Yes** means the request must include the session cookie. Without it, Flask-Login returns `401 Unauthorized`.

---

## 7. Running the Application

### Start the Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

On first run:
- Creates `expense_tracker.db` in the `backend/` folder
- Creates all tables (`users`, `budgets`, `expenses`)
- Seeds the database with demo user Vidhatri and 5 sample expenses
- Prints: `Database seeded — login: vidhatri@example.com / password123`
- Flask listens on `http://localhost:5000`

On subsequent runs:
- Tables already exist — `db.create_all()` is a no-op
- `seed_db()` sees `User.query.count() > 0` and returns immediately
- Server starts normally

### Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite starts a dev server at `http://localhost:5173`.

Open `http://localhost:5173` in a browser. Use the demo credentials or register a new account.
