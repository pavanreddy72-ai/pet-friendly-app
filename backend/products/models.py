from django.db import models


class Product(models.Model):
    CATEGORIES = [
        ("food", "Food"), ("treats", "Treats"), ("toys", "Toys"),
        ("bedding", "Beds & bedding"), ("grooming", "Grooming supplies"),
        ("health", "Health & hygiene"), ("accessories", "Collars, leashes & bowls"),
        ("travel", "Travel & carriers"), ("aquarium", "Aquarium supplies"),
        ("cage", "Cages & housing"), ("litter", "Litter & cleaning"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    pet_type = models.CharField(max_length=20, default="All")  # Dog, Cat, Dog & Cat, Small pets, Birds, Fish, Reptiles, All
    pack = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # INR, estimated
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "pet_type", "pack"], name="unique_product_variant"),
        ]

    def __str__(self):
        return f"{self.name} ({self.pack})"