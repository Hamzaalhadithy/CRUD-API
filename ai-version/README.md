# Tasks CRUD API

Simple FastAPI app with in-memory tasks.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

- `GET /` returns `Hello server`
- `GET /health` returns `{"status":"server is running"}`
- `GET /tasks` returns all tasks
- `GET /tasks/{id}` returns one task or `404`
- `POST /tasks` creates a task from `title`
- `PUT /tasks/{id}` updates `title` and/or `done`
- `DELETE /tasks/{id}` deletes a task
