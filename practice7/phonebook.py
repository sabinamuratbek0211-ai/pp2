import psycopg2
from config import load_config


def create_table():
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) UNIQUE NOT NULL
            );
        """)

        conn.commit()
        print("Table created successfully")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


create_table()

import csv

def insert_from_csv():
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()

        with open("contacts.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cur.execute("""
                    INSERT INTO phonebook (username, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (username) DO NOTHING;
                """, (row["username"], row["phone"]))

        conn.commit()
        print("CSV imported successfully")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

def insert_from_console():
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()

        username = input("Enter username: ")
        phone = input("Enter phone: ")

        cur.execute("""
            INSERT INTO phonebook (username, phone)
            VALUES (%s, %s);
        """, (username, phone))

        conn.commit()
        print("Inserted successfully")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

def update_contact():
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()

        old_username = input("Enter username to update: ")
        new_phone = input("Enter new phone: ")

        cur.execute("""
            UPDATE phonebook
            SET phone = %s
            WHERE username = %s;
        """, (new_phone, old_username))

        conn.commit()
        print("Updated successfully")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

def query_contacts():
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()

        name = input("Search by name: ")

        cur.execute("""
            SELECT * FROM phonebook
            WHERE username ILIKE %s;
        """, (f"%{name}%",))

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

def delete_contact():
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()

        username = input("Enter username to delete: ")

        cur.execute("""
            DELETE FROM phonebook
            WHERE username = %s;
        """, (username,))

        conn.commit()
        print("Deleted successfully")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

while True:
    print("\n1 - Insert")
    print("2 - Update")
    print("3 - Search")
    print("4 - Delete")
    print("5 - Exit")

    choice = input("Choose: ")

    if choice == "1":
        insert_from_console()
    elif choice == "2":
        update_contact()
    elif choice == "3":
        query_contacts()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        break

