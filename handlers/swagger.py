from fastapi import HTTPException, Depends
from app.models import NewTask, OldTask
from mySql import add_new_tasks, put_tasks, delete_tasks
from mySql import tasks_sql

def add_new_task(id: int, item: NewTask):
    if item.priority == 1:
        raise HTTPException(status_code=400, detail="Слишком низкий приоритет")
    return add_new_tasks(id, item)

def check_task(admin: str):
    return tasks_sql(admin)

def put_new_task(id: int, item: NewTask):
    return put_tasks(id,item)

def delete_task(id: int):
    return delete_tasks(id)

