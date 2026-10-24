# Accident Manager API (Backend)

An internal city administration tool for reporting, tracking, and resolving urban infrastructure incidents (potholes, traffic light failures, road works). Built with FastAPI and PostGIS.

## Tech Stack
* **Framework:** FastAPI (Python 3.11)
* **Database:** PostgreSQL with PostGIS extension
* **ORM:** SQLAlchemy 2.0 (Async) + GeoAlchemy2
* **Authentication:** JWT with Argon2id password hashing

## Architecture Notes
This system uses a strict 4-state administrative lifecycle (`pending`, `approved`, `rejected`, `resolved`). 
* **City Workers** use the API to report incidents in the field.
* **Dispatchers/Admins** use the API to review, approve, and resolve incidents.
* Database initialization and schema management are handled purely via raw SQL initialization scripts (`/database/init/`) mounted into the PostgreSQL Docker container. **We do not use Alembic.**

## Local Development Setup

1. **Configure Environment:**
   Copy the `.env` template:
   ```bash
   cp example.env .env
   ```
   Generate a secure JWT secret and add it to your `.env` file:
   ```bash
   openssl rand -hex 32
   ```

2. **Start the Infrastructure:**
   The entire stack (FastAPI, PostGIS) runs in Docker. 
   ```bash
   docker compose up --build -d
   ```
   *Note: The PostgreSQL container will automatically read the `01-schema.sql` and `02-seed.sql` files to build the tables and inject mock data on its first boot.*

3. **Access the API:**
   * **Interactive API Docs (Swagger UI):** http://localhost:8000/docs
   * **Health Check:** http://localhost:8000/health

## Test Accounts (from Seed Data)
* **Admin / Dispatcher:** `admin@urbanpulse.com` (Password: `Password2026!`)
* **City Worker:** `selim@student.com` (Password: `Password2026!`)

## Resetting the Database
If you need to wipe the database and start fresh with the seed data:
```bash
docker compose down -v
docker compose up --build -d
```