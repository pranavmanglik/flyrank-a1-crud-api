"""A small in-memory task API for Flyrank assignment W2 A1."""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

app = FastAPI(title="Task API", version="1.0")

# This version deliberately keeps tasks in memory, so restarting the server resets the examples.
tasks: list[dict[str, Any]] = [
    {"id": 1, "title": "Read the assignment brief", "done": False},
    {"id": 2, "title": "Build the API", "done": False},
    {"id": 3, "title": "Try Swagger UI", "done": True},
]

CREATE_TASK_BODY = {
    # The handlers read Request directly so they can return assignment-style 400 errors.
    # These schemas still let Swagger show the JSON body and its Try it out editor.
    "required": True,
    "content": {
        "application/json": {
            "schema": {
                "type": "object",
                "required": ["title"],
                "properties": {"title": {"type": "string", "minLength": 1}},
            },
            "example": {"title": "Buy milk"},
        }
    },
}
UPDATE_TASK_BODY = {
    "required": True,
    "content": {
        "application/json": {
            "schema": {
                "type": "object",
                "minProperties": 1,
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "done": {"type": "boolean"},
                },
            },
            "example": {"done": True},
        }
    },
}


def error(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": message})


async def read_object(request: Request) -> tuple[dict[str, Any] | None, str | None]:
    # Check the JSON shape ourselves so malformed bodies get a small, predictable error.
    try:
        body = await request.json()
    except Exception:
        return None, "Request body must be valid JSON"
    if not isinstance(body, dict):
        return None, "Request body must be a JSON object"
    return body, None


def find_task(task_id: int) -> dict[str, Any] | None:
    # Keep the lookup in one place so GET, PUT, and DELETE use the same rule.
    return next((task for task in tasks if task["id"] == task_id), None)


@app.get("/", summary="Describe the Task API")
def root() -> dict[str, Any]:
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Check that the API is running")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", summary="List tasks")
def list_tasks(done: bool | None = None, search: str | None = None) -> list[dict[str, Any]]:
    result = tasks
    if done is not None:
        # `is` compares booleans directly, so false tasks don't match true by accident.
        result = [task for task in result if task["done"] is done]
    if search:
        term = search.casefold()
        result = [task for task in result if term in task["title"].casefold()]
    return result


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error(f"Task {task_id} not found", 404)
    return task


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    openapi_extra={"requestBody": CREATE_TASK_BODY},
)
async def create_task(request: Request):
    body, issue = await read_object(request)
    if issue:
        return error(issue, 400)
    title = body.get("title")
    if not isinstance(title, str) or not title.strip():
        return error("Field 'title' is required and must be a non-empty string", 400)

    task = {
        # In memory, the next id is one greater than the largest id currently in the list.
        "id": max((item["id"] for item in tasks), default=0) + 1,
        "title": title.strip(),
        "done": False,
    }
    tasks.append(task)
    return JSONResponse(status_code=201, content=task)


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    openapi_extra={"requestBody": UPDATE_TASK_BODY},
)
async def update_task(task_id: int, request: Request):
    task = find_task(task_id)
    if task is None:
        return error(f"Task {task_id} not found", 404)

    body, issue = await read_object(request)
    if issue:
        return error(issue, 400)
    if not body or not set(body).intersection({"title", "done"}):
        return error("Provide a non-empty 'title' and/or a boolean 'done'", 400)
    if "title" in body:
        title = body["title"]
        if not isinstance(title, str) or not title.strip():
            return error("Field 'title' must be a non-empty string", 400)
        task["title"] = title.strip()
    if "done" in body:
        if not isinstance(body["done"], bool):
            return error("Field 'done' must be a boolean", 400)
        task["done"] = body["done"]
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error(f"Task {task_id} not found", 404)
    tasks.remove(task)
    return Response(status_code=204)


@app.get("/stats", summary="Count total, completed, and open tasks")
def stats() -> dict[str, int]:
    done_count = sum(task["done"] for task in tasks)
    return {"total": len(tasks), "done": done_count, "open": len(tasks) - done_count}
