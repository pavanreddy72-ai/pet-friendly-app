from django.db import models


class PetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    emoji = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "pet categories"

    def __str__(self):
        return self.name


class Breed(models.Model):
    category = models.ForeignKey(PetCategory, on_delete=models.PROTECT, related_name="breeds")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    # Basic characteristics
    origin = models.CharField(max_length=150, blank=True)
    purpose = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=100, blank=True)
    weight_range = models.CharField(max_length=100, blank=True)
    height_range = models.CharField(max_length=100, blank=True)
    lifespan = models.CharField(max_length=100, blank=True)
    adult_age = models.CharField(max_length=100, blank=True)

    # Behaviour and suitability
    temperament = models.CharField(max_length=300, blank=True)
    activity_level = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=100, blank=True)
    child_compatibility = models.CharField(max_length=200, blank=True)
    pet_compatibility = models.CharField(max_length=200, blank=True)
    purpose_tags = models.CharField(max_length=300, blank=True)
    suitable_for = models.CharField(max_length=300, blank=True)

    # Daily care
    diet = models.TextField(blank=True)
    grooming = models.TextField(blank=True)
    exercise_needs = models.TextField(blank=True)
    housing_needs = models.TextField(blank=True)
    social_needs = models.TextField(blank=True)
    care_needs = models.TextField(blank=True)
    care_difficulty = models.CharField(max_length=100, blank=True)

    # Health and welfare
    health_considerations = models.TextField(blank=True)
    enrichment = models.TextField(blank=True)
    legal_note = models.CharField(max_length=300, blank=True)

    # Image and visibility
    image_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["category", "name"], name="unique_breed_per_category"),
        ]

    def __str__(self):
        return f"{self.name} ({self.category.name})"