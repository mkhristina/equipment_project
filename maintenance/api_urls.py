
from rest_framework.routers import DefaultRouter

from .api_views import EquipmentViewSet, MaintenanceRequestViewSet


router = DefaultRouter()

router.register(
    "equipment",
    EquipmentViewSet,
    basename="equipment"
)

router.register(
    "requests",
    MaintenanceRequestViewSet,
    basename="maintenance-request"
)

urlpatterns = router.urls
