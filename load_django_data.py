
import json
import os

import django

from pathlib import Path


# Подключаем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from maintenance.models import Equipment, MaintenanceRequest


def load_equipment():
    """Загружает оборудование из equipment.json в базу Django."""

    file_path = Path(__file__).parent / "equipment.json"

    with open(file_path, "r", encoding="utf-8") as file:
        equipment_data = json.load(file)

    for item in equipment_data:
        Equipment.objects.update_or_create(
            inventory_number=item["inventory_number"],
            defaults={
                "name": item["name"],
                "equipment_type": item["equipment_type"],
                "department": item["department"],
                "production_year": item["production_year"],
                "status": item["status"],
            },
        )

    print(f"Загружено единиц оборудования: {len(equipment_data)}")


def load_requests():
    """Добавляет демонстрационные заявки."""

    examples = [
        {
            "inventory_number": "EQ-001",
            "description": "Повышенный шум при работе станка",
            "priority": "high",
            "status": "in_progress",
        },
        {
            "inventory_number": "EQ-002",
            "description": "Необходим ремонт фрезерного станка",
            "priority": "critical",
            "status": "in_progress",
        },
        {
            "inventory_number": "EQ-003",
            "description": "Проверка и техническое обслуживание компрессора",
            "priority": "low",
            "status": "new",
        },
    ]

    for item in examples:
        equipment = Equipment.objects.get(
            inventory_number=item["inventory_number"]
        )

        request, created = MaintenanceRequest.objects.get_or_create(
            equipment=equipment,
            description=item["description"],
            defaults={
                "priority": item["priority"],
                "status": item["status"],
            },
        )

        if created:
            print(f"Создана заявка №{request.id}")
        else:
            print(f"Заявка уже существует: №{request.id}")


def main():
    load_equipment()
    load_requests()

    print("\nЗагрузка данных завершена!")


if __name__ == "__main__":
    main()
