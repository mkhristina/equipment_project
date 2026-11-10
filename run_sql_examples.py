
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "db.sqlite3"
SQL_PATH = Path(__file__).parent / "sql_examples.sql"


def main():
    connection = sqlite3.connect(DB_PATH)

    try:
        with open(SQL_PATH, "r", encoding="utf-8") as file:
            sql_text = file.read()

        # Разделяем файл на отдельные SQL-запросы
        queries = [
            query.strip()
            for query in sql_text.split(";")
            if query.strip()
        ]

        for number, query in enumerate(queries, start=1):
            print(f"\n{'=' * 60}")
            print(f"РЕЗУЛЬТАТ ЗАПРОСА №{number}")
            print("=" * 60)

            cursor = connection.execute(query)

            # Названия столбцов
            columns = [description[0] for description in cursor.description]

            print(" | ".join(columns))
            print("-" * 60)

            # Результаты запроса
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(" | ".join(str(value) for value in row))
            else:
                print("Записей не найдено.")

        print("\nВсе SQL-запросы выполнены успешно!")

    except sqlite3.Error as error:
        print(f"Ошибка SQL: {error}")

    except FileNotFoundError as error:
        print(f"Файл не найден: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
