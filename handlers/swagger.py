from fastapi import HTTPException, Depends
from app.models import NewTask, OldTask
from database import add_new_tasks, check_tasks,put_tasks, delete_tasks

def add_new_task(id: int, item: NewTask):
    if item.priority == 1:
        raise HTTPException(status_code=400, detail="Слишком низкий приоритет")
    return add_new_tasks(id, item)

def check_task(admin: str):
    check_tasks(admin)

def put_new_task(id: int, item: NewTask):
    put_tasks(id,item)

def delete_task(id: int):
    return (id, item)

