# Accident Manager

A smart city incident tracking and management platform with role-based routing (Public/Admin), PostGIS spatial queries, and an interactive Leaflet map interface.

---

## Tech Stack

| Layer    | Technology |
|----------|------------|
| Database | PostgreSQL 16 + PostGIS (`postgis/postgis:16-3.4-alpine`) |
| Frontend | React 19 (TypeScript), Vite, Tailwind CSS v4, shadcn/ui, React Router, Leaflet / React-Leaflet, Zustand, TanStack Query |
| Backend  | Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0 (asyncpg), GeoAlchemy2, Uvicorn |

---

## Prerequisites

Make sure the following are installed on your machine:

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Node.js](https://nodejs.org/) (v20+ recommended)
- `npm` (bundled with Node.js)

---

## 1. Database Setup (Docker)

The database runs in a Docker container. On first boot it automatically initializes the PostGIS extension, creates the tables (`users`, `accidents`, `comments`), and loads seed mock data.

### Start the database

From the root of the repository:

```bash
docker compose up -d
```

> **Note:** Non-database services are currently commented out in `docker-compose.yml`, so this command launches only the PostGIS service.

### Verify database status

Check that the initialization scripts ran properly:

```bash
docker compose logs db
```

You should see output confirming that `/docker-entrypoint-initdb.d/01-schema.sql` and `02-seed.sql` were executed, ending with:

```text
database system is ready to accept connections
```

### Connect with the `psql` CLI

To inspect tables or run test queries inside the running container:

```bash
docker exec -it accident-manager-db psql -U admin -d accident_manager
```

Quick check queries:

```sql
-- Check mock users
SELECT email, role, is_active FROM users;

-- Check seeded incidents and coordinates
SELECT title, status, ST_AsText(location) AS coordinates FROM accidents;
```

Type `\q` and press Enter to exit.

### Reset / wipe database data

PostgreSQL only runs the scripts in `db/init-scripts/` when the storage volume is empty. If you change the schema or seed scripts, reset the volume:

```bash
docker compose down -v
docker compose up -d
```

---

## 2. Frontend Setup (Vite Dev Server)

The frontend runs locally with Vite hot-reloading for rapid UI development.

### Install dependencies

```bash
cd frontend
npm install
```

### Start the development server

```bash
npm run dev
```

Then open your browser at:

```text
http://localhost:5173
```

You should see the interactive incident map centered over Budapest, with the header controls.

---

## Project Structure

```text
accident-manager/
├── docker-compose.yml       # Orchestration file (DB active, backend/frontend stubs)
├── db/
│   └── init-scripts/
│       ├── 01-schema.sql    # Tables, PostGIS setup, enums, soft-delete flags
│       └── 02-seed.sql      # Mock users, Budapest incident coordinates, comments
├── backend/
│   ├── app/
│   │   ├── api/             # Shared API infrastructure
│   │   │   ├── dependencies.py  # Shared dependencies (e.g., get_db)
│   │   │   └── router.py        # Master router aggregating all features
│   │   ├── core/            # Global configs and infrastructure
│   │   │   └── database.py      # Async SQLAlchemy engine & session maker
│   │   ├── features/        # Feature-based modular business logic
│   │   │   └── accidents/
│   │   │       ├── models.py    # SQLAlchemy & GeoAlchemy2 table definitions
│   │   │       ├── router.py    # API endpoints (HTTP transport)
│   │   │       ├── schemas.py   # Pydantic validation models
│   │   │       └── service.py   # Business logic & PostGIS data conversions
│   │   └── main.py          # FastAPI application entry point
│   └── requirements.txt     
└── frontend/
    ├── src/
    │   ├── app/             
    │   │   ├── App.tsx      # QueryClient & Router providers
    │   │   └── routes.tsx   # Centralized React Router configuration
    │   ├── api/             # API client setup (Axios)
    │   ├── components/
    │   │   ├── layout/      # PublicLayout and AdminLayout shells
    │   │   └── ui/          # shadcn/ui primitives (Button, etc.)
    │   ├── features/
    │   │   └── map/         # Leaflet configuration and AccidentMap component
    │   ├── pages/           # Route views (MapPage, AdminDashboard)
    │   ├── store/           # Zustand state slices
    │   └── index.css        # Tailwind v4 setup & Leaflet container dimensions
    ├── package.json
    ├── tsconfig.app.json    # TypeScript compiler options & @/* path aliases
    └── vite.config.ts       # Vite bundler & Tailwind configuration
```

---

## Troubleshooting

**Port 5432 conflict**
If a local PostgreSQL service is already running on your host machine, stop it before running `docker compose up -d`, or change the host port mapping in `docker-compose.yml` (e.g., `"5433:5432"`).