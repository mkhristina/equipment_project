
from django.http import JsonResponse

from .models import Equipment, MaintenanceRequest


def statistics(request):
    total = Equipment.objects.count()

    broken = Equipment.objects.filter(
        status="repair"
    ).count()

    critical = MaintenanceRequest.objects.filter(
        priority="critical",
        status="new"
    ).count()

    return JsonResponse({
        "equipment_total": total,
        "equipment_in_repair": broken,
        "critical_open_requests": critical,
    })
