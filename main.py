from fastapi import FastAPI, status, Response
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: str | None=None
    done: bool | None=None


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
async def addTask(task: Task, response: Response):
    if not task.title:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error" : "The title is empty!"}

    new_task = {
        "id": tasks[-1]["id"] + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    response.status_code = status.HTTP_201_CREATED
    return new_task


@app.put("/tasks/{id}")
async def updateTask(id: int, updatedTask: UpdateTask, response: Response):
    if not updatedTask.title and not updatedTask.done:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error" : "Empty/Invalid Body"}
    
    for task in tasks:
        if task["id"] == id: 
            if updatedTask.title: task["title"] = updatedTask.title 
            if updatedTask.done: task["done"] = updatedTask.done
            return task
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Error": "Id Not Found"}
    

@app.delete("/tasks/{id}")
async def deleteTask(id: int, response:Response):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            response.status_code = status.HTTP_204_NO_CONTENT
            return 
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Error" : "Invalid ID"}

