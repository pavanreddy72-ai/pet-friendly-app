from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/listings/", include("listings.urls")),
    path("api/catalogue/", include("catalogue.urls")),
    path("api/pet-service/", include("pet_service.urls")),
    path("api/products/", include("products.urls")),
    path("api/vets/", include("vets.urls")),
    path("api/places/", include("places.urls")),
    path("api/pets/", include("pets.urls")),
    path("api/health/", include("health.urls")),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)