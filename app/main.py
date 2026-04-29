from fastapi import HTTPException, Depends, FastAPI
from app.auth import verify_admin
from app.models import NewTask, OldTask
from handlers.swagger import add_new_tasks, check_task,put_tasks,delete_tasks
import pymysql
from config import HOST,PASSWORD,DATABASE,USER

app = FastAPI()

def get_connection():
    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
        )
        return connection
    except Exception as ex:
        print(f"Connect error: {ex}")
        return None

@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks") # делаем запрос в таблицу tasks в базе
            rows = cursor.fetchall() # возвращаем список кортежей

            tasks = []
            for row in rows: # добавляем в список данные из дб
                tasks.append({
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "status": row[3]
                })
            return tasks # возвращаем список
    finally:
        connection.close()


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