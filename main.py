from fastapi import FastAPI, status, Response, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str 
    done: bool | None=None

class CreateTask(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: str | None=None
    done: bool | None=None


tasks = [
    Task(title='Task 1', done=False),
    Task(title='Task 2', done=True),
    Task(title='Task 3', done=False),
]

sqlite_url = f"sqlite:///tasks.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        exists = session.exec(select(Task)).first()
        if  (exists == None): 
            for task in tasks:
                session.add(task)
            session.commit()


@app.get("/")
async def root():
    """Return a simple description message"""
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@app.get("/health")
async def health():
    """Check System Health Status"""
    return {"status" : "ok"}


@app.get("/tasks", response_model=list[Task])
async def getTasks(session: SessionDep) -> list[Task]:
    """Return all the tasks"""
    tasks = session.exec(select(Task))
    return tasks

@app.get("/tasks/{taskid}", response_model=Task)
async def getTask(taskid: int, session: SessionDep) -> Task:
    """Return a specific task with id"""
    task = session.get(Task, taskid)
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return task


@app.post("/tasks", status_code=201)
async def addTask(task: CreateTask, session: SessionDep):
    """Add a new task"""
    if not task.title:
        raise HTTPException(status_code=400, detail="Missing Title")
    new_task = Task(title=task.title, done=False)
    session.add(new_task)
    session.commit()
    return "Task Created Successfully"



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

