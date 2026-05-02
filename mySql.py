import pymysql
from config import HOST,PASSWORD,DATABASE,USER
from app.models import NewTask
from fastapi import HTTPException

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

def read_expenses():
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


def save_expenses(task: NewTask):
    connection = get_connection()
    if not connection:
        return {"error":"Не удалось подключится к БД"}
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tasks (priority, title, description, status) VALUES (%s, %s, %s, %s)" # Делаем запрос в БД
            value = (task.priority, task.title, task.description, task.status) # Аргументы для Бд

            cursor.execute(sql,value) # выводим данные
            connection.commit()

            return {"message": "Данные успешно записаны в БД"}
    except Exception as e:
        return {"error": f"Ошибка при добавлении {e}"}
    finally:
        connection.close() # Закрываем Бд


def tasks_sql(admin:str):
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

def add_new_tasks(task: NewTask):
    connection = get_connection()
    if not connection:
        return {"error":"Не удалось подключится к БД"}
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tasks (priority, title, description, status) VALUES (%s, %s, %s, %s)" # Делаем запрос в БД
            values = (task.priority, task.title, task.description, task.status) # Аргументы для Бд

            cursor.execute(sql,values) # выводим данные
            connection.commit()

            return {"message": "Данные успешно записаны в БД"}
    except Exception as e:
        return {"error": f"Ошибка при добавлении {e}"}
    finally:
        connection.close() # Закрываем Бд


def put_tasks(id: int, item: NewTask):
   connection = get_connection()
   try:
       with connection.cursor() as cursor:
           cursor.execute("SELECT id FROM tasks WHERE id = %s", (id,)) # Берем только айди из БД
           if not cursor.fetchone():
               raise HTTPException(status_code=404, detail="Задача не найдена")

           sql = "UPDATE tasks SET title=%s, description=%s, status=%s WHERE id = %s" # Берем все элементы
           cursor.execute(sql, (item.title, item.description, item.status, id))
           connection.commit()

           return {"id": id,  **item.model_dump()}
   finally:
        connection.close()


def delete_tasks(id: int, admin: str):
    connection = get_connection()
    if not connection:
        return {"error": "Не удалось подключится к БД"}
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM tasks WHERE id = %s"  # Делаем запрос в БД
            cursor.execute(sql, (id,))  # выводим данные
            connection.commit()

            if cursor.rowcount == 0: # если равно 0 значит в базе нету записей удалять нечего
                return {"message":"Задача с таким id не найдена"}
            return {"message":f"Задача с id {id} удалена"}

    except Exception as e:
        return {"error": f"Ошибка при добавлении {e}"}
    finally:
        connection.close()  # Закрываем Бд