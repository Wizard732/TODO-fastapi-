from fastapi import HTTPException, Depends, FastAPI
from app.auth import verify_admin
from app.models import NewTask, OldTask
from handlers.swagger import add_new_tasks, check_task,put_tasks,delete_tasks
import pymysql
from config import HOST,PASSWORD,DATABASE,USER
from mySql import get_connection, tasks_sql

app = FastAPI()

def get_connect():
    return get_connection()

@app.get("/tasks")
def get_tasks():
    return tasks_sql()


@app.post("/new_task")
def add_task(task: NewTask):
    return add_new_tasks(task)

@app.get("/check_task")
def check_new_task(admin: str = Depends(verify_admin)):
    return check_task(admin)

@app.put("/expense/{id}")
def put_task(id: int, item: NewTask):
    return put_tasks(id,item)

@app.delete("/delete_task")
def delete_this_task(id: int, admin: str = Depends(verify_admin)):
    return delete_tasks(id,admin)