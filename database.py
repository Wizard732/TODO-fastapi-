import json
from json import JSONDecodeError
import pymysql
from mySql import get_connection
from app.models import NewTask, OldTask
from fastapi import HTTPException


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


def put_tasks(id: int, item: NewTask):
    data = read_expenses()
    found = False
    updated_index = -1

    for i in range(len(data)):
        if data[i]["id"] == id:
            new_data_dict = item.model_dump() # Создаем словарь из новых данных
            new_data_dict["id"] = id # Сохраняем старый ID, чтобы он не пропал
            data[i] = new_data_dict # Заменяем старый объект в списке на новый
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="Запись не найдена")
        # Сохраняем ВЕСЬ обновленный список
    save_expenses(data)
    return data[updated_index]

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








