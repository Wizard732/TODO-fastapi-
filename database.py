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


def check_tasks(admin: str):




def read_expenses():



def save_expenses(values):
    connection = get_connection()
    if not connection:
        return {"error":"Не удалось подключится к БД"}
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tasks (priority, title, description, status) VALUES (%s, %s, %s, %s)" # Делаем запрос в БД
            value = (values) # Аргументы для Бд

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

def delete_tasks(id: int,admin: str):
    data = read_expenses()
    filename = "main.json"
    new_list = []

    for task in data: # перебираем json файл если там есть задача не с айди который ввели перекидываем данные в новый файл
        if task["id"] != id:
            new_list.append(task)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_list,f) # вписываем данные с нового файла

    return  {"message":f"Задача{id} успешно удалена"}







