
from datetime import datetime


class MaintenanceRequest:
    ALLOWED_STATUSES = {"new", "in_progress", "completed", "cancelled"}
    ALLOWED_PRIORITIES = {"low", "medium", "high", "critical"}

    def __init__(self, request_id, equipment, description, priority="medium"):
        if not description.strip():
            raise ValueError("Описание заявки не может быть пустым")

        if priority not in self.ALLOWED_PRIORITIES:
            raise ValueError("Недопустимый приоритет")

        self.request_id = request_id
        self.equipment = equipment
        self.description = description
        self.priority = priority
        self.status = "new"
        self.created_at = datetime.now()

    def start(self):
        if self.status != "new":
            raise ValueError("В работу можно взять только новую заявку")

        self.status = "in_progress"

    def complete(self):
        if self.status != "in_progress":
            raise ValueError("Завершить можно только заявку в работе")

        self.status = "completed"

    def cancel(self):
        if self.status == "completed":
            raise ValueError("Завершённую заявку отменить нельзя")

        self.status = "cancelled"

    def change_priority(self, priority):
        if priority not in self.ALLOWED_PRIORITIES:
            raise ValueError("Недопустимый приоритет")

        self.priority = priority
