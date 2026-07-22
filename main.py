from fastapi import FastAPI, status, Response
from pydantic import BaseModel
import sqlite3


create_table_stm = """CREATE TABLE IF NOT EXISTS tasks( [ID] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, [Title] NVARCHAR(100) NOT NULL, [Done] INTEGER );"""
inset_exmps = """INSERT INTO tasks (Title, Done)  Values ('Task 1', 0), ('Task 2', 1), ('Task 3', 0) WHERE NOT EXISTS (SELEct 1 FROM tasks);"""
db = "tasks.db"
with sqlite3.connect(db) as conn:
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(create_table_stm)
    cur.execute(inset_exmps)
    conn.commit()
    print("tables created successfully")


app = FastAPI()

class CreateTask(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: str | None=None
    done: bool | None=None

class Task(BaseModel):
    id: int
    title: str
    done: bool | None=None
# 
# tasks = [
#     Task(id=1, title='Task 1', done=False),
#     Task(id=2, title='Task 2', done=False),
#     Task(id=3, title='Task 3', done=False),
# ]

@app.get("/")
async def root():
    """Return a simple description message"""
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@app.get("/health")
async def health():
    """Check System Health Status"""
    return {"status" : "ok"}


@app.get("/tasks")
async def getTasks():
    """Return all the tasks"""
    return tasks

@app.get("/tasks/{id}")
async def getTask(id: int, response:Response):
    """Return a specific task with id"""
    for task in tasks:
        if task.id == id:
            return task
        
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error" : f"Task {id} was not found"}


@app.post("/tasks")
async def addTask(task: CreateTask, response: Response):
    """Add a new task"""
    if not task.title:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error" : "The title is empty!"}

    new_task = Task(
        id = tasks[-1].id + 1,
        title = task.title,
        done= False
    )
    tasks.append(new_task)
    response.status_code = status.HTTP_201_CREATED
    return new_task


@app.put("/tasks/{id}")
async def updateTask(id: int, updatedTask: UpdateTask, response: Response):
    """Update a specific task with id"""
    if not updatedTask.title and not updatedTask.done:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error" : "Empty/Invalid Body"}
    
    for task in tasks:
        if task.id == id: 
            if updatedTask.title: task.title = updatedTask.title 
            if updatedTask.done: task.done = updatedTask.done
            return task
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Error": "Id Not Found"}
    

@app.delete("/tasks/{id}")
async def deleteTask(id: int, response:Response):
    """Delete a specific task with id"""
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            response.status_code = status.HTTP_204_NO_CONTENT
            return 
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Error" : "Invalid ID"}

