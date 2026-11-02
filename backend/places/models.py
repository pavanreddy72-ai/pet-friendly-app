from django.db import models


class Place(models.Model):
    CATEGORIES = [
        ("hotel", "Hotels"), ("resort", "Resorts & getaways"), ("restaurant", "Restaurants"),
        ("cafe", "Cafes"), ("park", "Parks"),
    ]
    UNITS = [("night", "per night"), ("for two", "for two"), ("entry", "entry")]

    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=15, choices=CATEGORIES)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, default="Bangalore")
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    pet_policy = models.CharField(max_length=300, blank=True)
    amenities = models.CharField(max_length=300, blank=True)  # comma separated
    price_min = models.PositiveIntegerField(default=0)  # INR
    price_max = models.PositiveIntegerField(default=0)
    price_unit = models.CharField(max_length=10, choices=UNITS, default="night")
    pet_fee = models.PositiveIntegerField(default=0)  # extra charge for bringing a pet
    is_sample = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "city", "area", "name"]

    def __str__(self):
        return self.name