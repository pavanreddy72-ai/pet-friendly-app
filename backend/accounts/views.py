
from typing import ClassVar

from rest_framework import generics, permissions
from rest_framework.throttling import AnonRateThrottle

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes: ClassVar[list[type[AnonRateThrottle]]] = [AnonRateThrottle]
