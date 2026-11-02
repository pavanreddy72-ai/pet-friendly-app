
from django.conf import settings
from django.db import models


class Pet(models.Model):
    class Species(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = "cat", "Cat"
        RABBIT = "rabbit", "Rabbit"
        GUINEA_PIG = "guinea_pig", "Guinea pig"
        HAMSTER = "hamster", "Hamster"
        BIRD = "bird", "Bird"
        FISH = "fish", "Fish"
        TORTOISE = "tortoise", "Tortoise"
        RAT = "rat", "Pet rat"
        CHINCHILLA = "chinchilla", "Chinchilla"
        OTHER = "other", "Other"

    class Sex(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        UNKNOWN = "unknown", "Unknown"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pets",
    )
    name = models.CharField(max_length=100)
    species = models.CharField(
        max_length=20,
        choices=Species.choices,
    )
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=10,
        choices=Sex.choices,
        default=Sex.UNKNOWN,
    )
    color = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"
