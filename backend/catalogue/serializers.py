from rest_framework import serializers

from .models import Breed, PetCategory


class PetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetCategory
        fields = ("id", "name", "slug", "description", "emoji")


class BreedSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    category_emoji = serializers.CharField(source="category.emoji", read_only=True)
    suitable_for_list = serializers.SerializerMethodField()

    class Meta:
        model = Breed
        fields = (
            "id", "name", "category", "category_name", "category_slug", "category_emoji",
            "description", "origin", "purpose", "size", "weight_range", "height_range",
            "lifespan", "adult_age", "temperament", "activity_level", "experience_level",
            "child_compatibility", "pet_compatibility", "suitable_for", "suitable_for_list",
            "diet", "grooming", "exercise_needs", "housing_needs", "social_needs",
            "care_needs", "care_difficulty", "health_considerations", "enrichment",
            "legal_note", "image_url",
        )

    def get_suitable_for_list(self, obj):
        return [t.strip() for t in obj.suitable_for.split(",") if t.strip()]