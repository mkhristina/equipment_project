
import sqlite3
from pathlib import Path

DB_PATH = Path("db.sqlite3")


def main():
    connection = sqlite3.connect(DB_PATH)

    try:
        print("ТАБЛИЦЫ В БАЗЕ ДАННЫХ:")

        tables = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """).fetchall()

        for table in tables:
            print("-", table[0])

        print("\nСТРУКТУРА ТАБЛИЦЫ EQUIPMENT:")

        columns = connection.execute("""
            PRAGMA table_info(maintenance_equipment)
        """).fetchall()

        for column in columns:
            print("-", column[1], "| тип:", column[2])

        print("\nСТРУКТУРА ТАБЛИЦЫ MAINTENANCE_REQUEST:")

        columns = connection.execute("""
            PRAGMA table_info(maintenance_maintenancerequest)
        """).fetchall()

        for column in columns:
            print("-", column[1], "| тип:", column[2])

        print("\nВНЕШНИЕ КЛЮЧИ:")

        foreign_keys = connection.execute("""
            PRAGMA foreign_key_list(
                maintenance_maintenancerequest
            )
        """).fetchall()

        for key in foreign_keys:
            print(
                key[3], "->",
                key[2] + "." + key[4]
            )

        print("\nПРОВЕРКА УНИКАЛЬНОСТИ:")

        indexes = connection.execute("""
            PRAGMA index_list(maintenance_equipment)
        """).fetchall()

        for index in indexes:
            if index[2]:
                print("-", index[1], "| уникальный индекс")

        print("\nПроверка базы данных завершена!")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
