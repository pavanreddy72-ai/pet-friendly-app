from rest_framework import filters, generics
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    """GET /api/products/?category=food&pet=Dog&search=puppy"""

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "category", "pet_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if params.get("category"):
            queryset = queryset.filter(category=params["category"])
        pet = params.get("pet")
        if pet:
            allowed = [pet, "All"]
            if pet in ("Dog", "Cat"):
                allowed.append("Dog & Cat")
            queryset = queryset.filter(pet_type__in=allowed)
        return queryset