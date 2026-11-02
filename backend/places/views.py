from django.db.models import Q
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny

from .models import Place
from .serializers import PlaceSerializer


class PlaceListView(generics.ListAPIView):
    """GET /api/places/?category=hotel&location=Indiranagar"""

    queryset = Place.objects.filter(is_active=True)
    serializer_class = PlaceSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "area", "city", "pet_policy", "amenities"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if params.get("category"):
            queryset = queryset.filter(category=params["category"])
        location = params.get("location")
        if location:
            queryset = queryset.filter(Q(area=location) | Q(city=location, area=""))
        return queryset