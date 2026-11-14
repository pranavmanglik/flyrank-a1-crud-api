# My first CRUD API

For this assignment, I built a small task API with FastAPI. I kept the tasks in memory so I could focus on learning the basic create, read, update, and delete operations before adding a database in a later project. That also means my tasks reset when I restart the server.

## What I added

- Routes to create, list, view, update, and delete tasks
- A health check at `/health`
- Optional `done` and `search` filters when listing tasks
- A `/stats` route for the total, completed, and open task counts
- Input checks and clear JSON errors for invalid requests or missing task IDs
- Swagger UI at `/docs`, which I used to explore the API

## How I run it

From this project folder, I set up the environment and start the server:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Then I open <http://localhost:8000/docs> to try the routes. The OpenAPI schema is available at <http://localhost:8000/openapi.json>.

## Routes

| Method | Path | What I use it for |
| --- | --- | --- |
| GET | `/` | Check the API name and version |
| GET | `/health` | Check that the API is running |
| GET | `/tasks` | List tasks, optionally filtering by `done` or `search` |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create a task, for example `{"title":"Buy milk"}` |
| PUT | `/tasks/{id}` | Update a task's `title`, `done` value, or both |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/stats` | Count all, completed, and open tasks |

The API returns `400` with a JSON error for invalid input, `404` when a task ID does not exist, and `204` after a successful delete.

## What I checked

I started the API and tried the health check and CRUD routes with `curl`. The health check returned `200`, creating a task returned `201`, and listing and updating tasks returned `200`. Deleting a task returned `204`.

I also restarted the server and listed the tasks again. My test task was gone, and the three starter tasks had been loaded again. That confirmed the in-memory reset behavior I expected for this version.

For example, I checked the list with:

```bash
curl -i http://localhost:8000/tasks
```

After the restart, it returned the three starter tasks: “Read the assignment brief”, “Build the API”, and “Try Swagger UI”.

## Terminal screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/00621359-e620-4ea8-a526-3bf532b6c19d" />

<!-- Add the screenshot here as assets/a1-crud-api-test.png once it is available in the project folder. -->

## What I want to improve next

This version is intentionally simple: restarting the server clears any tasks I created. In my SQLite project, I carry the same API idea forward and make the data persist. Before submitting this assignment, I still need to add my own Swagger screenshot and keep the genuine development commits that show how I built it step by step.

