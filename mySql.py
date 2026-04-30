import pymysql
from config import HOST,PASSWORD,DATABASE,USER

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

def tasks_sql():
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