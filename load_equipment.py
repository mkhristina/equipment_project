
import json
from models import Equipment


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

    print("Все оборудование:")
    for equipment in equipment_list:
        equipment.show_info()
        print()

    print("Оборудование, требующее ремонта:")
    for equipment in equipment_list:
        if equipment.needs_repair():
            print(
                equipment.inventory_number,
                "-",
                equipment.name,
                "-",
                equipment.status
            )


if __name__ == "__main__":
    main()
