
class Equipment:
    def __init__(self, inventory_number, name, equipment_type, department, production_year, status="working"):
        self.inventory_number = inventory_number
        self.name = name
        self.equipment_type = equipment_type
        self.department = department
        self.production_year = production_year
        self.status = status

    def show_info(self):
        print(f"Инвентарный номер: {self.inventory_number}")
        print(f"Название: {self.name}")
        print(f"Тип: {self.equipment_type}")
        print(f"Подразделение: {self.department}")
        print(f"Год выпуска: {self.production_year}")
        print(f"Состояние: {self.status}")

    def change_status(self, new_status):
        self.status = new_status

    def needs_repair(self):
        return self.status in {"repair", "broken"}
