
from django.contrib import admin
from .models import Equipment, MaintenanceRequest


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_number",
        "name",
        "department",
        "production_year",
        "status",
    )

    list_filter = (
        "status",
        "department",
    )

    search_fields = (
        "inventory_number",
        "name",
    )


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "equipment",
        "priority",
        "status",
        "created_at",
    )

    list_filter = (
        "priority",
        "status",
    )

    search_fields = (
        "description",
    )
