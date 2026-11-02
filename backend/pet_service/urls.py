from django.urls import path

from .views import (
    BookingCancelView,
    BookingDetailView,
    BookingListCreateView,
    PetServiceListView,
)

urlpatterns = [
    path("", PetServiceListView.as_view(), name="pet-service-list"),
    path("bookings/", BookingListCreateView.as_view(), name="pet-service-booking-list"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="pet-service-booking-detail"),
    path("bookings/<int:pk>/cancel/", BookingCancelView.as_view(), name="pet-service-booking-cancel"),
]