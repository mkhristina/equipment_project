
from models import Equipment
from maintenance_request import MaintenanceRequest
from service import MaintenanceService


def main():
    # Создаём оборудование
    machine = Equipment(
        inventory_number="EQ-001",
        name="Токарный станок 16К20",
        equipment_type="станок",
        department="Механический цех",
        production_year=2018
    )

    # Создаём первую заявку
    request1 = MaintenanceRequest(
        request_id=1,
        equipment=machine,
        description="Повышенный шум при работе",
        priority="high"
    )

    # Создаём вторую заявку
    request2 = MaintenanceRequest(
        request_id=2,
        equipment=machine,
        description="Перегрев двигателя",
        priority="critical"
    )

    # Создаём третью заявку
    request3 = MaintenanceRequest(
        request_id=3,
        equipment=machine,
        description="Плановая проверка оборудования",
        priority="low"
    )

    # Меняем статусы заявок
    request1.start()
    request1.complete()

    request2.start()

    # Создаём сервис заявок
    service = MaintenanceService()

    # Добавляем заявки в сервис
    service.add_request(request1)
    service.add_request(request2)
    service.add_request(request3)

    # Выводим все заявки
    print("Всего заявок:", len(service.get_all()))

    print("\nВсе заявки:")
    for request in service.get_all():
        print(
            f"Заявка №{request.request_id} | "
            f"Статус: {request.status} | "
            f"Приоритет: {request.priority} | "
            f"Описание: {request.description}"
        )

    # Ищем заявку по номеру
    print("\nПоиск заявки №2:")
    found_request = service.get_request(2)

    if found_request is not None:
        print(found_request.description)
    else:
        print("Заявка не найдена")

    # Фильтруем заявки по статусу
    print("\nЗаявки в работе:")
    for request in service.by_status("in_progress"):
        print(request.request_id, request.description)

    # Фильтруем заявки по приоритету
    print("\nЗаявки с критическим приоритетом:")
    for request in service.by_priority("critical"):
        print(request.request_id, request.description)


if __name__ == "__main__":
    main()
