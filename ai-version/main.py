from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Tasks CRUD API",
    description="A simple in-memory CRUD API for tasks.",
    version="1.0.0",
)


class Task(BaseModel):
    id: int
    name: str
    done: bool


class TaskCreateRequest(BaseModel):
    title: str = Field(..., description="Task title")


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, description="New task title")
    done: Optional[bool] = Field(None, description="Task completion status")


TASKS: list[Task] = [
    Task(id=1, name="Buy groceries", done=False),
    Task(id=2, name="Walk the dog", done=True),
    Task(id=3, name="Read a book", done=False),
]


def get_task_by_id(task_id: int) -> Task:
    for task in TASKS:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} doesn't exists",
    )


@app.get("/", summary="Root endpoint", response_class=PlainTextResponse)
def root() -> str:
    """Return a simple greeting from the server."""
    return "Hello server"


@app.get("/health", summary="Health check")
def health() -> dict[str, str]:
    """Return the server health status."""
    return {"status": "server is running"}


@app.get("/tasks", summary="List tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    """Return all tasks stored in memory."""
    return TASKS


@app.get("/tasks/{task_id}", summary="Get task by ID", response_model=Task)
def get_task(task_id: int) -> Task:
    """Return a single task by its ID."""
    return get_task_by_id(task_id)


@app.post(
    "/tasks",
    summary="Create task",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreateRequest) -> Task:
    """Create a new task with the next available ID."""
    title = payload.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="title cannot be empty",
        )

    next_id = max((task.id for task in TASKS), default=0) + 1
    task = Task(id=next_id, name=title, done=False)
    TASKS.append(task)
    return task


@app.put("/tasks/{task_id}", summary="Update task", response_model=Task)
def update_task(task_id: int, payload: TaskUpdateRequest) -> Task:
    """Update a task title and/or done status."""
    task = get_task_by_id(task_id)

    if payload.title is None and payload.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided",
        )

    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="title cannot be empty",
            )
        task.name = title

    if payload.done is not None:
        task.done = payload.done

    return task


@app.delete(
    "/tasks/{task_id}",
    summary="Delete task",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int) -> None:
    """Delete a task by its ID."""
    task = get_task_by_id(task_id)
    TASKS.remove(task)
    return None
