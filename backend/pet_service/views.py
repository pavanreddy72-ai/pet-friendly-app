from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, PetService
from .serializers import BookingCreateSerializer, BookingSerializer, PetServiceSerializer


def user_bookings(user):
    return (
        Booking.objects.filter(user=user)
        .select_related("invoice")
        .prefetch_related("items")
    )


class PetServiceListView(generics.ListAPIView):
    """GET /api/pet-service/?category=grooming&pet=Dog&size=Medium&search=bath"""

    queryset = PetService.objects.filter(is_active=True)
    serializer_class = PetServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "category"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if params.get("category"):
            queryset = queryset.filter(category=params["category"])
        if params.get("pet"):
            queryset = queryset.filter(pet_type__in=[params["pet"], PetService.PetType.BOTH])
        if params.get("size"):
            queryset = queryset.filter(size__in=[params["size"], PetService.Size.ANY])
        return queryset


class BookingListCreateView(generics.ListCreateAPIView):
    """GET = my bookings with invoices. POST = book services and receive the invoice."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return user_bookings(self.request.user)

    def get_serializer_class(self):
        return BookingCreateSerializer if self.request.method == "POST" else BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingDetailView(generics.RetrieveAPIView):
    """GET /api/pet-service/bookings/<id>/"""

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return user_bookings(self.request.user)


class BookingCancelView(APIView):
    """POST /api/pet-service/bookings/<id>/cancel/"""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = get_object_or_404(user_bookings(request.user), pk=pk)
        if booking.status != Booking.Status.CONFIRMED:
            return Response(
                {"detail": "Only confirmed bookings can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status"])
        return Response(BookingSerializer(booking).data)