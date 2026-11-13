# W2 A1 — Build your first CRUD API

A beginner-friendly in-memory task API using FastAPI. It includes the five CRUD routes, JSON error bodies, input validation, `/health`, `/stats`, filtering, search, and FastAPI's built-in Swagger UI at `/docs`. Data resets when the server restarts, as required for this assignment.

## Run

Use Python 3.10 or newer from this folder:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open <http://localhost:8000/docs> and try the endpoints. FastAPI also publishes the OpenAPI schema at `/openapi.json`.

## Endpoints

| Method | Path | Success | Purpose |
| --- | --- | --- | --- |
| GET | `/` | 200 | API name and version |
| GET | `/health` | 200 | Liveness |
| GET | `/tasks` | 200 | List; optional `done` and `search` filters |
| GET | `/tasks/{id}` | 200 | Read one task |
| POST | `/tasks` | 201 | Create with `{"title":"Buy milk"}` |
| PUT | `/tasks/{id}` | 200 | Update `title`, `done`, or both |
| DELETE | `/tasks/{id}` | 204 | Delete |
| GET | `/stats` | 200 | Count total, done, and open tasks |

Invalid bodies return 400 with `{"error":"..."}`. Unknown IDs return 404 with a JSON error.

## curl checkpoints

```bash
curl -i http://localhost:8000/tasks
curl -i http://localhost:8000/tasks/99
curl -i -X POST http://localhost:8000/tasks -H 'Content-Type: application/json' -d '{"title":"Buy milk"}'
curl -i -X PUT http://localhost:8000/tasks/1 -H 'Content-Type: application/json' -d '{"done":true}'
curl -i -X DELETE http://localhost:8000/tasks/1
```

After running these yourself, paste a genuine `curl -i` response here and add a Swagger screenshot before submission. Do not commit generated output as though it were observed if you have not run the API.

## Assignment steps

Suggested commits: hello server; root and health; read endpoints; create with validation; full CRUD; Swagger UI; README and publish. The optional AI rematch should be generated in a separate `ai-version/` folder or branch and compared by you. A public GitHub repo and real stage commits still need to be created for submission.
