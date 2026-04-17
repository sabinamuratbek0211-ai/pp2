import psycopg2

conn = psycopg2.connect(
    host: "localhost",
    port: "5432",
    dbname: "",
    user: "postgres",
    password: "12345678"
)

cur = conn.cursor()