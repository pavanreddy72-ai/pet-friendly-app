from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import HealthRecord
from .serializers import HealthRecordSerializer


class HealthRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = HealthRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HealthRecord.objects.filter(
            owner=self.request.user,
            pet__owner=self.request.user,
        ).select_related("pet")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HealthRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HealthRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HealthRecord.objects.filter(
            owner=self.request.user,
            pet__owner=self.request.user,
        ).select_related("pet")