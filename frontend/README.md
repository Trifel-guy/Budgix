# Budgix — Frontend

Vue.js 3 single-page application for the Budgix budget tracking platform.

## Stack

- **Vue.js 3** (Composition API + `<script setup>`)
- **Vite 5** for bundling and dev server
- **Pinia** for state management
- **Vue Router 4** with navigation guards
- **Tailwind CSS 3** for styling
- **ApexCharts** (`vue3-apexcharts`) for interactive charts
- **Axios** with automatic JWT refresh interceptor

## Structure

```
src/
├── api/
│   └── index.js           # Axios instance + all endpoint helpers
├── assets/
│   └── main.css           # Tailwind directives + component classes
├── components/
│   ├── layout/
│   │   ├── AppLayout.vue  # Sidebar + top bar shell
│   │   └── NavItem.vue    # Active-aware nav link
│   └── ui/
│       ├── SummaryCard.vue      # Metric card (income / expenses / balance)
│       ├── TransactionModal.vue # Create / edit transaction form
│       └── BudgetModal.vue      # Create budget form
├── router/
│   └── index.js           # Routes + auth/admin guards
├── stores/
│   └── auth.js            # Pinia store: login, logout, refresh, user
└── views/
    ├── auth/
    │   ├── LoginView.vue
    │   └── RegisterView.vue
    ├── admin/
    │   ├── AdminDashboardView.vue   # Platform stats + radial gauge
    │   └── AdminUsersView.vue       # User list + enable/disable
    ├── DashboardView.vue     # Summary cards + donut + bar charts
    ├── TransactionsView.vue  # Table with filters, pagination, CRUD
    ├── BudgetsView.vue       # Progress bars + radial overview
    ├── CategoriesView.vue    # Cards grouped by income/expense
    └── ImportView.vue        # Drag & drop CSV/Excel + result report
```

## Setup

```bash
npm install
npm run dev       # dev server → http://localhost:5173
npm run build     # production build → dist/
npm run preview   # preview production build locally
npm run lint      # ESLint
```

## Environment Variables

Create a `.env.local` file (not committed):

```env
VITE_API_URL=/api/v1
```

In development the Vite proxy forwards `/api` requests to `http://localhost:8000` (configured in `vite.config.js`).

## Key Design Decisions

**Auth flow** — The Axios interceptor catches 401 responses, silently refreshes the access token via the refresh token, retries the original request, and redirects to `/login` only if the refresh itself fails. This is handled in `src/api/index.js`.

**Route guards** — `router/index.js` checks `isAuthenticated` before every navigation. Admin routes additionally check `isAdmin`. The user profile is lazy-loaded on the first authenticated navigation.

**Charts** — All charts are ApexCharts instances driven by computed properties that react to the selected month/year. Data is fetched with `Promise.all` to minimise waterfall loading.

**Utility classes** — Common patterns (`.card`, `.btn-primary`, `.input`, `.badge-income`) are defined as Tailwind `@layer components` in `main.css` to avoid repetition across templates.

## Docker

```bash
# Build production image
docker build -t budgix-frontend .

# Run (serves on port 80)
docker run -p 80:80 budgix-frontend
```

The Dockerfile builds the Vite app then serves it via Nginx. The `nginx.conf` handles SPA routing (fallback to `index.html`) and proxies `/api/` to the backend container.

## CSV Import Template

| Column        | Required | Notes                          |
|---------------|----------|--------------------------------|
| `date`        | ✅       | `YYYY-MM-DD`                   |
| `amount`      | ✅       | Positive number, e.g. `49.99`  |
| `type`        | ✅       | `income` or `expense`          |
| `description` | ✅       | Max 255 chars                  |
| `category`    | —        | Must match an existing category name |
| `tags`        | —        | Comma-separated                |
| `note`        | —        | Free text                      |

Use the **Download template** button on the Import page to get a pre-filled CSV example.
