
from rest_framework import serializers

from .models import Equipment, MaintenanceRequest


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = "__all__"
        read_only_fields = ("id", "created_at")

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Описание заявки не может быть пустым."
            )
        return value.strip()


class PriorityUpdateSerializer(serializers.Serializer):
    priority = serializers.ChoiceField(
        choices=MaintenanceRequest.PRIORITY_CHOICES
    )
