from fastapi import FastAPI, status, Response
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

tasks = [
    {"id": 1, "title" : "Task 1", "done" : False},
    {"id": 2, "title" : "Task 2", "done" : True},
    {"id": 3, "title" : "Task 3", "done" : False},
]
@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@app.get("/health")
async def health():
    return {"status" : "ok"}


@app.get("/tasks")
async def getTasks():
    return tasks

@app.get("/tasks/{id}")
async def getTask(id: int, response:Response):
    for task in tasks:
        if task["id"] == id:
            return task
        
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error" : f"Task {id} was not found"}


@app.post("/tasks")
async def addTask(payload: TaskCreate, response: Response):
    if not payload.title:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error" : "The title is empty!"}

    new_task = {
        "id": tasks[-1]["id"] + 1,
        "title": payload.title,
        "done": False
    }
    tasks.append(new_task)
    response.status_code = status.HTTP_201_CREATED
    return new_task


