import psycopg2
import csv
from config import params

def execute_query(sql, data=None, fetch=False):
    
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, data)
                if fetch:
                    return cur.fetchall()
                conn.commit()
    except Exception as e:
        print(f"Ошибка базы данных: {e}")

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        user_name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20) NOT NULL
    );
    """
    execute_query(sql)
    print("Таблица проверена/создана.")

def insert_contact(name, phone):
    sql = "INSERT INTO contacts (user_name, phone_number) VALUES (%s, %s);"
    execute_query(sql, (name, phone))

def upload_from_csv(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row: # если строка не пустая
                    insert_contact(row[0], row[1])
        print(f"Данные из {file_path} успешно загружены!")
    except FileNotFoundError:
        print("Файл CSV не найден. Создайте contacts.csv")

def get_contacts(filter_name=None):
    if filter_name:
        sql = "SELECT * FROM contacts WHERE user_name ILIKE %s;"
        return execute_query(sql, (f"%{filter_name}%",), fetch=True)
    return execute_query("SELECT * FROM contacts;", fetch=True)

def delete_contact(name):
    sql = "DELETE FROM contacts WHERE user_name = %s;"
    execute_query(sql, (name,))