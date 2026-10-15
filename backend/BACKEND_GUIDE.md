# Accident Manager Backend Guide

Reference for the frontend team: **local setup, authentication, incident lifecycle and REST API contracts**.

## Quick start

The stack is **FastAPI + Python 3.11**, **PostgreSQL 16 + PostGIS**, **SQLAlchemy**, **Alembic** and **JWT authentication**. Docker Compose runs the API and database. The React frontend runs separately using Vite.

**1. Configure the backend** from the repository root:

```powershell
# Windows PowerShell
Copy-Item backend/example.env backend/.env
python -c "import secrets; print(secrets.token_hex(32))"
```

```bash
# macOS / Linux
cp backend/example.env backend/.env
openssl rand -hex 32
```

Copy the generated secret into `JWT_SECRET_KEY` in `backend/.env`. Keep the provided `DATABASE_URL` host `db:5432` when running inside Docker. Never commit `.env`.

**2. Start and inspect services:**

```bash
docker compose up --build -d
docker compose ps
docker compose logs --tail=50 backend
```

**3. Open the API:**

| Service | Local URL |
| --- | --- |
| API documentation / Swagger | http://localhost:8000/docs |
| OpenAPI JSON | http://localhost:8000/openapi.json |
| Database health check | http://localhost:8000/health |
| Frontend development server | http://localhost:5173 |

`GET /health` should return `{"status":"healthy","database":"connected"}`.

### Database migrations

The backend runs pending Alembic migrations automatically when its Docker container starts. To apply or inspect them manually:

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend alembic current
docker compose exec backend alembic heads
```

On a freshly initialised database, `alembic current` should report `0001_community_review (head)`.

**Schema ownership:** Alembic's `0001_community_review.py` creates the complete schema from an empty PostgreSQL database: the PostGIS extension, `users`, `accidents`, `comments`, `incident_confirmations`, `notification_events`, their relationships, indexes and status enums. PostgreSQL's container creates the empty database; no `db/init-scripts` or seed files run. Therefore, the public incident list is initially empty, and there are no preconfigured users or passwords. Register a user with the API or create an administrator using the command below.

**Reset the local development database from scratch** (Windows PowerShell, macOS or Linux):

```bash
# DESTRUCTIVE: removes the project's PostgreSQL volume and ALL its data.
docker compose down -v
docker compose up --build -d
docker compose ps
docker compose exec backend alembic current
```

The backend runs `alembic upgrade head` automatically at startup. There is no need to execute it manually after a successful fresh start. Use `docker compose logs --tail=100 backend` to inspect any startup or migration errors.

**If the backend container did not start:** check `docker compose logs backend` first. Once it is running, `docker compose exec backend alembic upgrade head` applies any outstanding migration.

**Existing databases:** Alembic will not re-run a revision that PostgreSQL has already recorded as applied, even if the migration file changed. These instructions deliberately discard the local database. Never run `down -v` against a shared or valuable database; retain data with a new forward migration instead.

## Authentication and access

Public registration always creates a regular `user`. Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

| Action | Endpoint | JSON request body |
| --- | --- | --- |
| Register | `POST /api/auth/register` | `{"name":"Alex Morgan","email":"alex@example.org","password":"ExamplePassword2026!"}` |
| Log in | `POST /api/auth/login` | `{"email":"alex@example.org","password":"ExamplePassword2026!"}` |
| Get profile | `GET /api/auth/me` | None; requires JWT |
| Update name | `PATCH /api/users/me` | `{"name":"Alex M."}`; requires JWT |

**Login uses JSON, not form-data**, and returns:

```json
{"access_token":"<jwt>","token_type":"bearer"}
```

Registration requires a name of 2–80 characters and a password of 10–128 characters. The access token expires after 60 minutes by default; refresh tokens are not implemented. User profiles return `id`, `name`, `email`, `role`, `is_active` and `created_at`, without password hashes.

| Actor | Permitted actions |
| --- | --- |
| **Guest** | View approved incidents, read public comments |
| **Signed-in user** | Report, confirm nearby pending reports, view own reports, comment, edit/delete own pending reports |
| **Admin** | All relevant user actions plus approve/reject/resolve incidents, moderate reports and delete comments |

Create an administrator through the server, **not** public registration. The command creates or updates the account and its password:

```bash
docker compose exec -e ADMIN_EMAIL=admin@example.org -e ADMIN_PASSWORD="CHOOSE_A_LONG_UNIQUE_PASSWORD" backend python -m app.scripts.create_admin
```

## Incident lifecycle

There is **one** incident state field: `status`. The frontend should use these exact values:

| `status` | Meaning | Assigned by | Public active map |
| --- | --- | --- | --- |
| `pending` | Awaiting verification | Backend at creation | No |
| `approved` | Verified for publication | Admin or community | Yes |
| `rejected` | Invalid report | Admin only | No |
| `resolved` | Considered finished | Admin only | No |

```text
pending ──> approved ──> resolved
   │            │
   └──> rejected <┘
```

- New reports are `pending`. The reporter counts as **one** confirmation.
- At `COMMUNITY_THRESHOLD=5`, four **other distinct accounts** can confirm a nearby pending incident and approve it automatically. The admin can approve without waiting.
- Only the admin can reject or resolve. An admin may reject an already approved incident.
- `rejected` and `resolved` are final; invalid transitions return `409 Conflict`.
- `verification_source` (`admin`, `community` or `null`) records how approval happened; it is **not** a second status.
- `resolved` means an administrator marked the issue as finished; the system does not assign repair teams or track municipal work.

**The single admin status endpoint** is:

```http
PATCH /api/admin/accidents/{incident_id}/status
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

Body: `{"status":"approved"}`, `{"status":"rejected"}` or `{"status":"resolved"}`. `pending` cannot be sent through this endpoint. An invalid value returns `422`; an invalid transition returns `409`.

## API endpoints

Exactly **one entry per method and route**. IDs in paths are UUIDs. A JWT is required wherever indicated.

| Method | Route | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/health` | Public | Health check |
| `POST` | `/api/auth/register` | Public | Register |
| `POST` | `/api/auth/login` | Public | Log in |
| `GET` | `/api/auth/me` | JWT | Current user |
| `PATCH` | `/api/users/me` | JWT | Update own name |
| `GET` | `/api/accidents/` | Public | Approved active incidents; optional map bounds |
| `GET` | `/api/accidents/nearby` | Public | Approved incidents within a radius |
| `GET` | `/api/accidents/pending-nearby` | JWT | Pending nearby incidents for confirmation |
| `GET` | `/api/accidents/similar` | JWT | Possible duplicate reports |
| `GET` | `/api/accidents/mine` | JWT | Own report history |
| `GET` | `/api/accidents/{incident_id}` | Public for approved/resolved; otherwise reporter/admin | Incident detail |
| `POST` | `/api/accidents/` | JWT | Create incident |
| `POST` | `/api/accidents/{incident_id}/confirmations` | JWT | Confirm pending incident |
| `PATCH` | `/api/accidents/{incident_id}` | Reporter/admin; pending only | Edit incident (resets confirmations) |
| `DELETE` | `/api/accidents/{incident_id}` | Reporter for pending; admin for any | Soft-delete incident |
| `GET` | `/api/admin/accidents/` | Admin JWT | List reports by status |
| `PATCH` | `/api/admin/accidents/{incident_id}/status` | Admin JWT | Approve, reject or resolve |
| `GET` | `/api/accidents/{incident_id}/comments` | According to incident visibility | List comments |
| `POST` | `/api/accidents/{incident_id}/comments` | JWT | Create comment on active approved incident |
| `GET` | `/api/comments/{comment_id}` | According to incident visibility | Comment detail |
| `PATCH` | `/api/comments/{comment_id}` | Author JWT | Edit own comment |
| `DELETE` | `/api/comments/{comment_id}` | Author/admin JWT | Soft-delete comment |

### Map filters and query parameters

| Endpoint | Parameters |
| --- | --- |
| `GET /api/accidents/` | Optional `west,south,east,north` (provide all four); `limit=100` (max 200), `offset=0` |
| `GET /api/accidents/nearby` | Required `lat,lng`; `radius_m=500` (20–10,000 metres) |
| `GET /api/accidents/pending-nearby` | Required `lat,lng`; `radius_m=500` (20–1,000 metres) |
| `GET /api/accidents/similar` | Required `lat,lng,category`; `radius_m=100` (20–200 metres), last 48 hours |
| `GET /api/accidents/mine` | `limit=100` (max 200), `offset=0` |
| `GET /api/admin/accidents/` | `status=pending` by default; also `approved`, `rejected`, `resolved`; `limit=100` (max 200) |
| `GET /api/accidents/{incident_id}/comments` | `limit=50` (max 100), `offset=0` |

**Leaflet map viewport:**

```http
GET /api/accidents/?west=19.01&south=47.48&east=19.07&north=47.52
```

**Incidents within 2 km:**

```http
GET /api/accidents/nearby?lat=47.4979&lng=19.0402&radius_m=2000
```

The public list shows only `approved`, non-expired, non-deleted incidents. `resolved` incidents are excluded from the active list but their historical details can still be read using their IDs.

### Incident payloads

**Create:** `POST /api/accidents/` (requires JWT)

```json
{
  "title": "Broken traffic light",
  "description": "The junction lights are not working",
  "category": "traffic_light",
  "severity": "medium",
  "coordinates": [47.4979, 19.0402]
}
```

- Categories: `accident`, `road_work`, `road_closure`, `pothole`, `traffic_light`, `other`.
- Severity: `low`, `medium`, `high`.
- Title: 5–160 characters. Description: optional, max 2,000 characters.
- Optional `starts_at` and `ends_at`: timezone-aware ISO 8601 timestamps.
- **API coordinates use `[latitude, longitude]` (Leaflet order).** PostGIS stores longitude–latitude internally (SRID 4326).
- The backend generates the UUID and assigns `reporter_id`, `status` and confirmation count. Do **not** send those fields on creation.

**Incident response** (illustrative, the real IDs are generated automatically):

```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "reporter_id": "81e7b1c2-1b43-47d4-92c9-7659113183c9",
  "title": "Broken traffic light",
  "description": "The junction lights are not working",
  "category": "traffic_light",
  "severity": "medium",
  "status": "approved",
  "verification_source": "community",
  "confirmations_count": 5,
  "required_confirmations": 5,
  "is_deleted": false,
  "coordinates": [47.4979, 19.0402],
  "starts_at": null,
  "ends_at": null,
  "created_at": "2026-10-15T12:00:00Z",
  "updated_at": "2026-10-15T12:00:00Z"
}
```

**Confirm:** `POST /api/accidents/{incident_id}/confirmations` (different authenticated user)

```json
{"coordinates":[47.4979,19.0402]}
```

The server checks account age, duplicate confirmations and the submitted position against `CONFIRMATION_MAX_DISTANCE_M`. Client-provided GPS coordinates are not independently verified.

### Comment payloads

`POST /api/accidents/{incident_id}/comments` and `PATCH /api/comments/{comment_id}` accept:

```json
{"content":"The road is still blocked."}
```

Comments are 1–2,000 characters. Responses contain `id`, `accident_id`, `author_id`, `author_name`, `content`, `created_at` and `updated_at` (never the author's email). Visitors may read comments on approved/resolved incidents. Only authenticated users may write on **approved, non-expired** incidents. The author can edit a comment; the author or an admin can soft-delete it. Resolved incidents retain readable comments but cannot receive new ones.

## Frontend integration notes

- Use `http://localhost:8000` as the Axios base URL and `Content-Type: application/json` for request bodies.
- After login, attach `Authorization: Bearer <access_token>` to protected requests; fetch `/api/auth/me` to obtain the user and `role`.
- Replace `MOCK_INCIDENTS` with `GET /api/accidents/`. Use map bounds or `/nearby` instead of loading every incident.
- Fetch `/api/accidents/mine` for the profile's report history. Pending reports do not appear in the public map.
- Before creating a report, `/api/accidents/similar` can help suggest an existing one. Show `/pending-nearby` to signed-in users who wish to confirm reports.
- Admin screens should use `/api/admin/accidents/?status=pending` and update statuses with the single `PATCH .../status` endpoint.
- Read comments when opening an incident's details panel. Deletions return `204 No Content`.
- Hiding admin UI is useful, but the **backend's authorisation checks** remain the security boundary.

## Configuration and troubleshooting

| Environment variable (`backend/.env`) | Purpose | Typical local value |
| --- | --- | --- |
| `DATABASE_URL` | Postgres connection inside Docker | `postgresql+asyncpg://admin:secretpassword@db:5432/accident_manager` |
| `JWT_SECRET_KEY` | Secret for signing JWTs | Random value, minimum 32 characters |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT lifetime | `60` |
| `COMMUNITY_THRESHOLD` | Total independent confirmations | `5` |
| `CONFIRMATION_MAX_DISTANCE_M` | Confirmation proximity threshold | `500` |
| `MIN_ACCOUNT_AGE_HOURS` | Minimum account age to confirm | `0` for student demos |
| `MAX_REPORTS_PER_HOUR` | Per-user hourly report limit | `5` |

| HTTP code | Meaning |
| --- | --- |
| `200` / `201` / `204` | Success / created / success without body |
| `401` | Missing, invalid or expired token |
| `403` | Insufficient permissions or failed confirmation checks |
| `404` | Not found or not visible to the caller |
| `409` | Duplicate confirmation or invalid state transition |
| `422` | Invalid request body, path or query parameters |
| `429` | Hourly reporting limit reached |
| `503` | Database unavailable in the health check |

If the backend does not start, check `docker compose logs --tail=100 backend`, the database health in `docker compose ps` and `backend/.env`. Missing database columns usually indicate unapplied migrations. If React shows a CORS error, check `CORS_ORIGINS` (including the port). `GET /` and `/favicon.ico` returning `404` is expected; use `/docs` or `/health`.
