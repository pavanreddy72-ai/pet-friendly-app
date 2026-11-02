
from rest_framework import serializers

from pets.models import Pet
from .models import HealthRecord


class HealthRecordSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(
        source="pet.name",
        read_only=True,
    )

    class Meta:
        model = HealthRecord
        fields = (
            "id",
            "pet",
            "pet_name",
            "record_type",
            "title",
            "date",
            "next_due_date",
            "veterinarian",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "pet_name",
            "created_at",
            "updated_at",
        )

    def validate_pet(self, pet):
        request = self.context.get("request")

        if request and pet.owner_id != request.user.id:
            raise serializers.ValidationError(
                "You can only add health records for your own pets."
            )

        return pet

    def validate(self, attrs):
        date = attrs.get("date", getattr(self.instance, "date", None))
        next_due_date = attrs.get(
            "next_due_date",
            getattr(self.instance, "next_due_date", None),
        )

        if date and next_due_date and next_due_date < date:
            raise serializers.ValidationError({
                "next_due_date": "The next due date cannot be before the record date."
            })

        return attrs