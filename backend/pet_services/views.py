from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Booking, Service
from .serializers import BookingCreateSerializer, BookingSerializer, ServiceSerializer


class ServiceListView(generics.ListAPIView):
    """GET /api/services/?category=grooming&pet=Dog"""

    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "category", "size"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if params.get("category"):
            queryset = queryset.filter(category=params["category"])
        if params.get("pet"):
            queryset = queryset.filter(pet_type__in=[params["pet"], "Dog & Cat"])
        return queryset


class BookingListCreateView(generics.ListCreateAPIView):
    """GET = my bookings with invoices. POST = book services and get an invoice."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Booking.objects.filter(user=self.request.user)
                .select_related("invoice").prefetch_related("items"))

    def get_serializer_class(self):
        return BookingCreateSerializer if self.request.method == "POST" else BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Booking.objects.filter(user=self.request.user)
                .select_related("invoice").prefetch_related("items"))