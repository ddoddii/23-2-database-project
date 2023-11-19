import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ny2790827!",
    database="QADatabase"
)

cursor = conn.cursor()

cursor.execute("SHOW TABLES")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
