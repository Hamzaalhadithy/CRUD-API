from fastapi import FastAPI, status, Response


app = FastAPI()

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
