
import json
import sqlite3


def add_test_data(connection):
    # Загружаем оборудование из equipment.json
    with open("equipment.json", "r", encoding="utf-8") as file:
        equipment_data = json.load(file)

    for item in equipment_data:
        connection.execute("""
            INSERT OR IGNORE INTO equipment (
                inventory_number,
                name,
                equipment_type,
                department,
                production_year,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["inventory_number"],
            item["name"],
            item["equipment_type"],
            item["department"],
            item["production_year"],
            item["status"]
        ))

    # Добавляем тестовые заявки, если таблица пока пустая
    request_count = connection.execute(
        "SELECT COUNT(*) FROM maintenance_request"
    ).fetchone()[0]

    if request_count == 0:
        equipment = connection.execute("""
            SELECT id FROM equipment ORDER BY id LIMIT 3
        """).fetchall()

        if len(equipment) < 3:
            raise ValueError("В базе должно быть минимум 3 единицы оборудования.")

        test_requests = [
            (equipment[0][0], "Повышенный шум при работе", "high", "in_progress"),
            (equipment[1][0], "Необходим ремонт станка", "critical", "in_progress"),
            (equipment[2][0], "Плановая проверка компрессора", "low", "new")
        ]

        connection.executemany("""
            INSERT INTO maintenance_request (
                equipment_id,
                description,
                priority,
                status
            )
            VALUES (?, ?, ?, ?)
        """, test_requests)

    connection.commit()


def show_results(connection, title, query):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    cursor = connection.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("Записей нет.")
        return

    for row in rows:
        print(row)


def main():
    connection = sqlite3.connect("equipment.db")

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        add_test_data(connection)

        # ЗАПРОС 1. Список заявок по приоритету
        show_results(
            connection,
            "1. ЗАЯВКИ ПО ПРИОРИТЕТУ",
            """
            SELECT
                maintenance_request.id,
                equipment.name,
                maintenance_request.description,
                maintenance_request.priority,
                maintenance_request.status
            FROM maintenance_request
            JOIN equipment
                ON maintenance_request.equipment_id = equipment.id
            ORDER BY
                CASE maintenance_request.priority
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                END
            """
        )

        # ЗАПРОС 2. Количество заявок по статусам
        show_results(
            connection,
            "2. КОЛИЧЕСТВО ЗАЯВОК ПО СТАТУСАМ",
            """
            SELECT status, COUNT(*) AS request_count
            FROM maintenance_request
            GROUP BY status
            ORDER BY request_count DESC
            """
        )

        # ЗАПРОС 3. Оборудование без активных заявок
        show_results(
            connection,
            "3. ОБОРУДОВАНИЕ БЕЗ АКТИВНЫХ ЗАЯВОК",
            """
            SELECT
                equipment.inventory_number,
                equipment.name
            FROM equipment
            LEFT JOIN maintenance_request
                ON equipment.id = maintenance_request.equipment_id
                AND maintenance_request.status IN ('new', 'in_progress')
            WHERE maintenance_request.id IS NULL
            """
        )

        # ЗАПРОС 4. Самое проблемное оборудование
        show_results(
            connection,
            "4. САМОЕ ПРОБЛЕМНОЕ ОБОРУДОВАНИЕ",
            """
            SELECT
                equipment.inventory_number,
                equipment.name,
                COUNT(maintenance_request.id) AS request_count
            FROM equipment
            JOIN maintenance_request
                ON equipment.id = maintenance_request.equipment_id
            GROUP BY equipment.id
            ORDER BY request_count DESC
            """
        )

        print("\nВсе четыре SQL-запроса выполнены!")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
