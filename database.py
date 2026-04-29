import json
from json import JSONDecodeError

from app.models import NewTask, OldTask
from fastapi import HTTPException


def add_new_tasks(task: NewTask):
    filename = "main.json"

    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if not data:
        new_id = 1 # если в json еще не было данных с id 1 создаем id 1
    else:
        new_id = data[-1]["id"] +1 # если данные были берем последнее айди и прибавляем +1
    new_expense = task.model_dump()
    new_expense["id"] = new_id # передаем данные с new id в new expense
    data.append(new_expense) # добавляем в data данные с new expense

    try:
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(data, f)
    except OSError:
        return {'error': "Не удалось записать данные в файл"}

def check_tasks(admin: str):
    filename = "main.json"

    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"message": "Не удалось открыть файл"}
    return data


def read_expenses():
    filename = "main.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(data):
    filename = "main.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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







