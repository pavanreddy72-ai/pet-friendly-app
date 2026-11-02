from django.conf import settings
from django.db import models


class HealthRecord(models.Model):
    class RecordType(models.TextChoices):
        VACCINATION = "vaccination", "Vaccination"
        VET_VISIT = "vet_visit", "Vet visit"
        MEDICATION = "medication", "Medication"
        TREATMENT = "treatment", "Treatment"
        CHECKUP = "checkup", "Routine checkup"
        OTHER = "other", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="health_records",
    )
    pet = models.ForeignKey(
        "pets.Pet",
        on_delete=models.CASCADE,
        related_name="health_records",
    )
    record_type = models.CharField(
        max_length=20,
        choices=RecordType.choices,
        default=RecordType.CHECKUP,
    )
    title = models.CharField(max_length=150)
    date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    veterinarian = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.pet.name}: {self.title}"