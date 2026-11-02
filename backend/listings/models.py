from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class ListingBase(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending review"
        ACTIVE = "active", "Active"
        RESERVED = "reserved", "Reserved"
        COMPLETED = "completed", "Completed"
        REJECTED = "rejected", "Rejected"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        UNKNOWN = "unknown", "Not sure"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_listings",
    )
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=100, blank=True)
    age_description = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.UNKNOWN)
    vaccinated = models.BooleanField(default=False)
    neutered = models.BooleanField(default=False)
    description = models.TextField()
    location = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to="listings/%Y/%m/", blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AdoptionListing(ListingBase):
    adoption_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Adoption: {self.pet_name}"


class SaleListing(ListingBase):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"For sale: {self.pet_name}"