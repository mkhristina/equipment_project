
import json
from models import Equipment
from maintenance_request import MaintenanceRequest
from service import MaintenanceService


def load_equipment(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    equipment_list = []

    for item in data:
        equipment = Equipment(
            inventory_number=item["inventory_number"],
            name=item["name"],
            equipment_type=item["equipment_type"],
            department=item["department"],
            production_year=item["production_year"],
            status=item["status"]
        )

        equipment_list.append(equipment)

    return equipment_list


def main():
    equipment_list = load_equipment("equipment.json")

    service = MaintenanceService()

    request1 = MaintenanceRequest(
        request_id=1,
        equipment=equipment_list[0],
        description="Повышенный шум при работе",
        priority="high"
    )

    request2 = MaintenanceRequest(
        request_id=2,
        equipment=equipment_list[1],
        description="Необходим ремонт станка",
        priority="critical"
    )

    request3 = MaintenanceRequest(
        request_id=3,
        equipment=equipment_list[2],
        description="Плановая проверка компрессора",
        priority="low"
    )

    request1.start()
    request2.start()

    service.add_request(request1)
    service.add_request(request2)
    service.add_request(request3)

    print("Открытые заявки с приоритетом high или critical:")

   
    report_lines = [
        "ОТЧЁТ ПО ЗАЯВКАМ НА ОБСЛУЖИВАНИЕ",
        ""
    ]

    for request in service.get_all():
        if (
            request.status in {"new", "in_progress"}
            and request.priority in {"high", "critical"}
        ):
            line = (
                f"Заявка №{request.request_id} | "
                f"Оборудование: {request.equipment.name} | "
                f"Приоритет: {request.priority} | "
                f"Статус: {request.status}"
            )

            print(line)
            report_lines.append(line)

    with open("report.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(report_lines))

    print("\nОтчёт сохранён в report.txt")



if __name__ == "__main__":
    main()


