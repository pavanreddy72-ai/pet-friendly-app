
from rest_framework import generics, permissions
from rest_framework.throttling import AnonRateThrottle

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # noqa: RUF012
    throttle_classes = [AnonRateThrottle]  # noqa: RUF012
