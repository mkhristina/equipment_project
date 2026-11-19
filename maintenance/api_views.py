
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Equipment, MaintenanceRequest
from .serializers import (
    EquipmentSerializer,
    MaintenanceRequestSerializer,
    PriorityUpdateSerializer,
)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all().order_by("id")
    serializer_class = EquipmentSerializer


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.select_related(
        "equipment"
    ).all().order_by("-created_at")

    serializer_class = MaintenanceRequestSerializer

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        maintenance_request = self.get_object()

        if maintenance_request.status != "new":
            return Response(
                {"error": "Начать можно только новую заявку."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        maintenance_request.status = "in_progress"
        maintenance_request.save(update_fields=["status"])

        return Response(
            self.get_serializer(maintenance_request).data
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        maintenance_request = self.get_object()

        if maintenance_request.status != "in_progress":
            return Response(
                {"error": "Завершить можно только заявку в работе."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        maintenance_request.status = "completed"
        maintenance_request.save(update_fields=["status"])

        return Response(
            self.get_serializer(maintenance_request).data
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        maintenance_request = self.get_object()

        if maintenance_request.status in ["completed", "cancelled"]:
            return Response(
                {"error": "Эту заявку нельзя отменить."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        maintenance_request.status = "cancelled"
        maintenance_request.save(update_fields=["status"])

        return Response(
            self.get_serializer(maintenance_request).data
        )

    @action(detail=True, methods=["post"], url_path="change-priority")
    def change_priority(self, request, pk=None):
        maintenance_request = self.get_object()

        serializer = PriorityUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        maintenance_request.priority = serializer.validated_data["priority"]
        maintenance_request.save(update_fields=["priority"])

        return Response(
            self.get_serializer(maintenance_request).data
        )
