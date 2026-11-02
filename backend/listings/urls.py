from django.urls import path

from .views import (
    AdoptionListingDetailView,
    AdoptionListingListCreateView,
    SaleListingDetailView,
    SaleListingListCreateView,
)

app_name = "listings"

urlpatterns = [
    path("adoptions/", AdoptionListingListCreateView.as_view(), name="adoption-list"),
    path("adoptions/<int:pk>/", AdoptionListingDetailView.as_view(), name="adoption-detail"),
    path("sales/", SaleListingListCreateView.as_view(), name="sale-list"),
    path("sales/<int:pk>/", SaleListingDetailView.as_view(), name="sale-detail"),
]