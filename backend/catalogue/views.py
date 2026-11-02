from rest_framework import filters, generics
from rest_framework.permissions import AllowAny

from .models import Breed, PetCategory
from .serializers import BreedSerializer, PetCategorySerializer


class PetCategoryListView(generics.ListAPIView):
    queryset = PetCategory.objects.filter(is_active=True)
    serializer_class = PetCategorySerializer
    permission_classes = [AllowAny]


class BreedListView(generics.ListAPIView):
    """GET /api/catalogue/breeds/?category=dog&suitable=Guard&search=shepherd"""

    queryset = Breed.objects.filter(is_active=True, category__is_active=True).select_related("category")
    serializer_class = BreedSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "category__name", "suitable_for", "temperament", "origin"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if params.get("category"):
            queryset = queryset.filter(category__slug=params["category"])
        if params.get("suitable"):
            queryset = queryset.filter(suitable_for__icontains=params["suitable"])
        return queryset