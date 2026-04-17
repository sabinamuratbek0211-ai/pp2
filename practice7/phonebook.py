cur.execute("SELECT * FROM phonebook")
rows = cur.fetchall()

for row in rows:
    print(row)