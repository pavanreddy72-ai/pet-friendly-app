from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class PetService(models.Model):
    """A service the business offers, priced per hour / day / night / session / visit / trip."""

    class Category(models.TextChoices):
        WALKING = "walking", "Dog walking"
        GROOMING = "grooming", "Grooming"
        BOARDING = "boarding", "Boarding"
        DAYCARE = "daycare", "Day care & pet sitting"
        FOOD = "food", "Food & meals"
        TRAINING = "training", "Training"
        VET = "vet", "Vet & health"
        TRANSPORT = "transport", "Pet transport"

    class Unit(models.TextChoices):
        HOUR = "hour", "per hour"
        DAY = "day", "per day"
        NIGHT = "night", "per night"
        SESSION = "session", "per session"
        VISIT = "visit", "per visit"
        TRIP = "trip", "per trip"

    class PetType(models.TextChoices):
        DOG = "Dog", "Dog"
        CAT = "Cat", "Cat"
        BOTH = "Dog & Cat", "Dog & Cat"

    class Size(models.TextChoices):
        ANY = "Any", "Any size"
        SMALL = "Small", "Small"
        MEDIUM = "Medium", "Medium"
        LARGE = "Large", "Large"
        GIANT = "Giant", "Giant"

    category = models.CharField(max_length=20, choices=Category.choices)
    name = models.CharField(max_length=150)
    pet_type = models.CharField(max_length=20, choices=PetType.choices, default=PetType.DOG)
    size = models.CharField(max_length=10, choices=Size.choices, default=Size.ANY)
    unit = models.CharField(max_length=10, choices=Unit.choices)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )  # INR
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name", "price"]
        constraints = [
            models.UniqueConstraint(fields=["name", "pet_type", "size"], name="unique_pet_service_variant"),
        ]
        indexes = [models.Index(fields=["category", "is_active"])]

    def __str__(self):
        return f"{self.name} ({self.size}) - {self.price}/{self.unit}"


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pet_service_bookings"
    )
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=20, blank=True)
    pet_name = models.CharField(max_length=100, blank=True)
    service_date = models.DateField(default=timezone.localdate)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "-created_at"])]

    def __str__(self):
        return f"Booking {self.pk} - {self.customer_name}"


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(PetService, on_delete=models.PROTECT, related_name="+")
    # Snapshots, so an old invoice never changes when prices change later
    service_name = models.CharField(max_length=200)
    unit = models.CharField(max_length=10)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.5")), MaxValueValidator(Decimal("365"))],
    )  # hours, days, nights, sessions...
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service_name} x {self.quantity}"


class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="invoice")
    number = models.CharField(max_length=30, unique=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self):
        return self.number