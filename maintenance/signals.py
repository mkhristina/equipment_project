
from django.db.models.signals import post_save
from django.dispatch import receiver

from .audit import log_event
from .models import Equipment, MaintenanceRequest


@receiver(post_save, sender=Equipment)
def equipment_audit(sender, instance, created, **kwargs):
    event_type = "created" if created else "updated"

    log_event(
        event_type=event_type,
        model_name="Equipment",
        object_id=instance.pk,
        details={
            "inventory_number": instance.inventory_number,
            "name": instance.name,
            "status": instance.status,
        },
    )


@receiver(post_save, sender=MaintenanceRequest)
def maintenance_request_audit(sender, instance, created, **kwargs):
    event_type = "created" if created else "updated"

    log_event(
        event_type=event_type,
        model_name="MaintenanceRequest",
        object_id=instance.pk,
        details={
            "equipment_id": instance.equipment_id,
            "description": instance.description,
            "priority": instance.priority,
            "status": instance.status,
        },
    )
