from django.urls import path

from .views import HospitalListView, MedicationListView

urlpatterns = [
    path("hospitals/", HospitalListView.as_view(), name="hospital-list"),
    path("medications/", MedicationListView.as_view(), name="medication-list"),
]