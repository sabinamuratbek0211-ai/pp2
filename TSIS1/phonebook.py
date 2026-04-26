import csv
import json
from connect import get_connection


def print_contacts(rows):
    if not rows:
        print("No contacts found")
        return

    for row in rows:
        print("-" * 50)
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Email: {row[2]}")
        print(f"Birthday: {row[3]}")
        print(f"Group: {row[4]}")
        print(f"Phones: {row[5]}")
        print(f"Created at: {row[6]}")


def search():
    query = input("Search by name/email/phone/group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    print_contacts(rows)

    cur.close()
    conn.close()


def filter_by_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '') AS phones,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    """, (group,))

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def sort_contacts():
    print("Sort by:")
    print("1 Name")
    print("2 Birthday")
    print("3 Date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        print("Wrong choice")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '') AS phones,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order_by}
    """)

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def add_or_update_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group = input("Group Family/Work/Friend/Other: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL upsert_contact_extended(%s, %s, %s, %s, %s, %s)",
        (name, email, birthday, group, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact saved")


def add_phone():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Contact moved")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def paginated_navigation():
    limit = int(input("Page size: "))
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                c.id,
                c.name,
                c.email,
                c.birthday,
                g.name,
                COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '') AS phones,
                c.created_at
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()
        print_contacts(rows)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ").lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Wrong command")


def export_json():
    filename = input("JSON filename: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
    """)

    contacts = []

    for contact in cur.fetchall():
        contact_id = contact[0]

        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
        """, (contact_id,))

        phones = [
            {"phone": p[0], "type": p[1]}
            for p in cur.fetchall()
        ]

        contacts.append({
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]) if contact[3] else None,
            "group": contact[4],
            "phones": phones
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Export completed")


def import_json():
    filename = input("JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for contact in contacts:
        name = contact["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        exists = cur.fetchone()

        if exists:
            action = input(f"{name} already exists. skip/overwrite: ")

            if action == "skip":
                continue
            elif action == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
            else:
                print("Skipped because wrong action")
                continue

        phones = contact.get("phones", [])

        if phones:
            first_phone = phones[0]
            cur.execute(
                "CALL upsert_contact_extended(%s, %s, %s, %s, %s, %s)",
                (
                    contact["name"],
                    contact.get("email"),
                    contact.get("birthday"),
                    contact.get("group"),
                    first_phone["phone"],
                    first_phone["type"]
                )
            )

            for phone in phones[1:]:
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (contact["name"], phone["phone"], phone["type"])
                )
        else:
            cur.execute(
                "CALL upsert_contact_extended(%s, %s, %s, %s, %s, %s)",
                (
                    contact["name"],
                    contact.get("email"),
                    contact.get("birthday"),
                    contact.get("group"),
                    None,
                    None
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Import completed")


def import_csv():
    filename = input("CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute(
                "CALL upsert_contact_extended(%s, %s, %s, %s, %s, %s)",
                (
                    row["name"],
                    row["email"],
                    row["birthday"],
                    row["group"],
                    row["phone"],
                    row["phone_type"]
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import completed")


while True:
    print("\nPHONEBOOK MENU")
    print("1 Search")
    print("2 Filter by group")
    print("3 Sort contacts")
    print("4 Add / Update contact")
    print("5 Add phone")
    print("6 Move to group")
    print("7 Paginated navigation")
    print("8 Export to JSON")
    print("9 Import from JSON")
    print("10 Import from CSV")
    print("11 Exit")

    choice = input("Choose: ")

    if choice == "1":
        search()
    elif choice == "2":
        filter_by_group()
    elif choice == "3":
        sort_contacts()
    elif choice == "4":
        add_or_update_contact()
    elif choice == "5":
        add_phone()
    elif choice == "6":
        move_to_group()
    elif choice == "7":
        paginated_navigation()
    elif choice == "8":
        export_json()
    elif choice == "9":
        import_json()
    elif choice == "10":
        import_csv()
    elif choice == "11":
        break
    else:
        print("Wrong choice")