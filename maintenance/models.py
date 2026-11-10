
from django.db import models


class Equipment(models.Model):
    STATUS_CHOICES = [
        ("working", "Исправно"),
        ("repair", "Требует ремонта"),
        ("broken", "Неисправно"),
    ]

    inventory_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    equipment_type = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    production_year = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="working"
    )

    def __str__(self):
        return f"{self.inventory_number} — {self.name}"


class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Низкий"),
        ("medium", "Средний"),
        ("high", "Высокий"),
        ("critical", "Критический"),
    ]

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
    ]

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка №{self.id}"
