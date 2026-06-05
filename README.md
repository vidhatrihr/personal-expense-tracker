# Personal Expense Tracker

<p align="center">
  <img src="assets/screenshot-1.png" alt="Personal Expense Tracker" width="75%" />
</p>

A full-stack expense tracking application where users can set a monthly budget, log expenses, and view a spending summary.

**Stack:** Flask · SQLite · Vue 3 (Vite)

---

## Project Structure

```
personal-expense-tracker/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── populate_db.py
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py
│       └── expenses.py
└── frontend/
    └── src/
        ├── composables/
        │   └── useWhoAmI.js
        ├── utils/
        │   └── api.js
        ├── router/
        │   └── index.js
        ├── views/
        │   ├── LoginView.vue
        │   ├── RegisterView.vue
        │   └── DashboardView.vue
        ├── App.vue
        ├── main.js
        └── style.css
```

---

## Routes

| Path         | View            | Description                            |
| ------------ | --------------- | -------------------------------------- |
| `/`          | `LoginView`     | Login page                             |
| `/register`  | `RegisterView`  | Registration page                      |
| `/dashboard` | `DashboardView` | Budget, expenses, and spending summary |

### API endpoints

| Method   | URL                  | Description          |
| -------- | -------------------- | -------------------- |
| `POST`   | `/api/register`      | Create account       |
| `POST`   | `/api/login`         | Log in               |
| `POST`   | `/api/logout`        | Log out              |
| `GET`    | `/api/whoami`        | Current user info    |
| `GET`    | `/api/budget`        | Get current budget   |
| `POST`   | `/api/budget`        | Set or update budget |
| `GET`    | `/api/expenses`      | List all expenses    |
| `POST`   | `/api/expenses`      | Add an expense       |
| `DELETE` | `/api/expenses/<id>` | Delete an expense    |

---

## Running the Application

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Runs on `http://localhost:5000`. On first run, creates the database and seeds demo data.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:5173`.

---

## Screenshots

<table>
  <tr>
    <td><img src="assets/screenshot-1.png" alt="Screenshot 1" /></td>
    <td><img src="assets/screenshot-2.png" alt="Screenshot 2" /></td>
  </tr>
  <tr>
    <td><img src="assets/screenshot-3.png" alt="Screenshot 3" /></td>
  </tr>
</table>
