
from django.urls import include, path

from .views import statistics


urlpatterns = [
    path("statistics/", statistics, name="statistics"),
    path("api/", include("maintenance.api_urls")),
]
