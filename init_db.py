
import sqlite3

with open("schema.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

connection = sqlite3.connect("equipment.db")

try:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(sql_script)
    connection.commit()

    print("База данных успешно создана!")
    print("Таблицы equipment и maintenance_request созданы.")

finally:
    connection.close()
