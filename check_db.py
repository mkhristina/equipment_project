
import sqlite3

connection = sqlite3.connect("equipment.db")

try:
    connection.execute("PRAGMA foreign_keys = ON")

    print("ТАБЛИЦЫ В БАЗЕ ДАННЫХ:")

    tables = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """).fetchall()

    for table in tables:
        print("-", table[0])

    print("\nСТОЛБЦЫ ТАБЛИЦЫ equipment:")

    columns = connection.execute(
        "PRAGMA table_info(equipment)"
    ).fetchall()

    for column in columns:
        print("-", column[1])

    print("\nСТОЛБЦЫ ТАБЛИЦЫ maintenance_request:")

    columns = connection.execute(
        "PRAGMA table_info(maintenance_request)"
    ).fetchall()

    for column in columns:
        print("-", column[1])

    print("\nВНЕШНИЕ КЛЮЧИ:")

    foreign_keys = connection.execute(
        "PRAGMA foreign_key_list(maintenance_request)"
    ).fetchall()

    for key in foreign_keys:
        print(
            f"{key[3]} -> {key[2]}.{key[4]}"
        )

finally:
    connection.close()
