from django.urls import path

from .views import HealthRecordDetailView, HealthRecordListCreateView

app_name = "health"

urlpatterns = [
    path("", HealthRecordListCreateView.as_view(), name="health-list-create"),
    path("<int:pk>/", HealthRecordDetailView.as_view(), name="health-detail"),
]