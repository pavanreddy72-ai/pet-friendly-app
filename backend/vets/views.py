from rest_framework import filters, generics
from rest_framework.permissions import AllowAny

from .models import Hospital, Medication
from .serializers import HospitalSerializer, MedicationSerializer


class HospitalListView(generics.ListAPIView):
    """GET /api/vets/hospitals/?area=Koramangala&emergency=1&home=1"""

    queryset = Hospital.objects.filter(is_active=True)
    serializer_class = HospitalSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "area", "services", "city"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if params.get("area"):
            queryset = queryset.filter(area=params["area"])
        if params.get("emergency") == "1":
            queryset = queryset.filter(emergency_24x7=True)
        if params.get("home") == "1":
            queryset = queryset.filter(home_visits=True)
        return queryset


class MedicationListView(generics.ListAPIView):
    """GET /api/vets/medications/?category=parasite&pet=Dog"""

    queryset = Medication.objects.filter(is_active=True)
    serializer_class = MedicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "used_for", "category", "form"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if params.get("category"):
            queryset = queryset.filter(category=params["category"])
        pet = params.get("pet")
        if pet:
            allowed = [pet]
            if pet in ("Dog", "Cat"):
                allowed.append("Dog & Cat")
            queryset = queryset.filter(pet_type__in=allowed)
        return queryset