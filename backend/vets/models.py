from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=200, unique=True)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Bangalore")
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    services = models.CharField(max_length=400, blank=True)  # comma separated
    pet_types = models.CharField(max_length=100, default="Dogs, Cats")
    open_hours = models.CharField(max_length=100, blank=True)
    emergency_24x7 = models.BooleanField(default=False)
    home_visits = models.BooleanField(default=False)
    consultation_fee_min = models.PositiveIntegerField(default=0)  # INR
    consultation_fee_max = models.PositiveIntegerField(default=0)
    is_sample = models.BooleanField(default=True)  # untick in /admin after you verify real details
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["area", "name"]

    def __str__(self):
        return self.name


class Medication(models.Model):
    CATEGORIES = [
        ("deworming", "Deworming"), ("parasite", "Tick & flea"), ("skin", "Skin care"),
        ("wound", "Wound care"), ("ear", "Ear care"), ("eye", "Eye care"),
        ("supplement", "Vitamins & supplements"), ("digestive", "Digestive care"),
        ("vaccine", "Vaccines"), ("prescription", "Prescription medicines"),
        ("aquarium", "Aquarium treatment"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    pet_type = models.CharField(max_length=20, default="Dog & Cat")
    form = models.CharField(max_length=60, blank=True)
    used_for = models.CharField(max_length=300, blank=True)
    price_min = models.PositiveIntegerField(default=0)  # INR, estimated, medicine only
    price_max = models.PositiveIntegerField(default=0)
    prescription_required = models.BooleanField(default=False)
    notes = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "pet_type"], name="unique_medication_variant"),
        ]

    def __str__(self):
        return self.name