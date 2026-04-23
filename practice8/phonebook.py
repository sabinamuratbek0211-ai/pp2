from connect import get_connection

def search():
    pattern = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)

    conn.close()


def upsert():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    conn.close()


def delete():
    name = input("Name (or empty): ")
    phone = input("Phone (or empty): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s, %s)", (name or None, phone or None))
    conn.commit()

    print("Deleted successfully")
    
    conn.close()


def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)

    conn.close()


while True:
    print("\n1 Search")
    print("2 Upsert")
    print("3 Delete")
    print("4 Pagination")
    print("5 Exit")

    c = input("Choose: ")

    if c == "1":
        search()
    elif c == "2":
        upsert()
    elif c == "3":
        delete()
    elif c == "4":
        pagination()
    elif c == "5":
        break