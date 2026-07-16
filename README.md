# Task API

This is a small FastAPI task tracker. It exposes a handful of CRUD endpoints for working with an in-memory list of tasks, plus a health check and a root metadata route.

## Install & Run

```bash
python -m venv .venv && source .venv/bin/activate && pip install fastapi uvicorn pydantic && uvicorn main:app --host 127.0.0.1 --port 8000
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Returns API metadata and the list of documented endpoints. |
| GET | `/health` | Returns a simple health status payload. |
| GET | `/tasks` | Returns all tasks. |
| GET | `/tasks/{id}` | Returns one task by id or `404` if it does not exist. |
| POST | `/tasks` | Creates a new task from JSON like `{"title":"Buy milk"}`. |
| PUT | `/tasks/{id}` | Updates an existing task's `title` and/or `done` fields. |
| DELETE | `/tasks/{id}` | Deletes a task by id. |

## Example `curl -i`

```bash
HTTP/1.1 201 Created
date: Thu, 16 Jul 2026 12:04:59 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger Screenshot

![Swagger UI](swagger-ui.png)