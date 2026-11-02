from django.db.models import Q
from rest_framework import filters, generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import AdoptionListing, SaleListing
from .serializers import AdoptionListingSerializer, SaleListingSerializer


class IsOwnerOrReadOnly(BasePermission):
    """Allow everyone to read listings, but only owners/admins to edit."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or obj.owner_id == request.user.id)
        )


class OwnerListingQuerysetMixin:
    """
    List filters (all optional):
      ?search=  ?species=Dog  ?location=Bangalore  ?gender=male
      ?vaccinated=1  ?max_price=5000  ?mine=1  ?ordering=-created_at
    """

    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["pet_name", "species", "breed", "description", "location"]
    ordering_fields = ["created_at", "pet_name"]
    ordering = ["-created_at"]
    price_field = "price"  # overridden for adoption listings

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        params = self.request.query_params
        is_list = "pk" not in self.kwargs
        mine = params.get("mine") == "1" and user.is_authenticated

        if mine:
            queryset = queryset.filter(owner=user)
        elif user.is_authenticated and user.is_staff:
            pass
        elif is_list:
            queryset = queryset.filter(status="active")
        elif user.is_authenticated:
            queryset = queryset.filter(Q(status="active") | Q(owner=user))
        else:
            queryset = queryset.filter(status="active")

        if is_list:
            if params.get("species"):
                queryset = queryset.filter(species__iexact=params["species"])
            if params.get("location"):
                queryset = queryset.filter(location__icontains=params["location"])
            if params.get("gender"):
                queryset = queryset.filter(gender=params["gender"])
            if params.get("vaccinated") == "1":
                queryset = queryset.filter(vaccinated=True)
            if params.get("max_price"):
                try:
                    queryset = queryset.filter(
                        **{f"{self.price_field}__lte": params["max_price"]}
                    )
                except (ValueError, TypeError):
                    pass
        return queryset


class AdoptionListingListCreateView(OwnerListingQuerysetMixin, generics.ListCreateAPIView):
    queryset = AdoptionListing.objects.select_related("owner")
    serializer_class = AdoptionListingSerializer
    price_field = "adoption_fee"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status="active")


class AdoptionListingDetailView(OwnerListingQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = AdoptionListing.objects.select_related("owner")
    serializer_class = AdoptionListingSerializer
    price_field = "adoption_fee"


class SaleListingListCreateView(OwnerListingQuerysetMixin, generics.ListCreateAPIView):
    queryset = SaleListing.objects.select_related("owner")
    serializer_class = SaleListingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status="active")


class SaleListingDetailView(OwnerListingQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = SaleListing.objects.select_related("owner")
    serializer_class = SaleListingSerializer