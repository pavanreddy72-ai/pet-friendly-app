
from rest_framework import serializers

from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
      model = Pet
      fields = [
            "id",
            "name",
            "species",
            "breed",
            "date_of_birth",
            "sex",
            "color",
            "description",
            "created_at",
            "updated_at",
        ]
    read_only_fields = ["id", "created_at", "updated_at"]
