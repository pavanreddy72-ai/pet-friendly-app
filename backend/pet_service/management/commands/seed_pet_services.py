from decimal import Decimal

from django.core.management.base import BaseCommand

from pet_service.models import PetService

# (category, name, pet_type, size, unit, price in INR). Estimates; edit them in /admin.
SERVICES = [
    # Walking (per hour)
    ("walking", "Dog walking", "Dog", "Small", "hour", 200),
    ("walking", "Dog walking", "Dog", "Medium", "hour", 250),
    ("walking", "Dog walking", "Dog", "Large", "hour", 350),
    ("walking", "Group dog walk", "Dog", "Any", "hour", 150),
    ("walking", "Puppy walk & potty training", "Dog", "Any", "hour", 300),
    ("walking", "Jogging with your dog", "Dog", "Any", "hour", 400),
    # Grooming (per session)
    ("grooming", "Bath & blow dry", "Dog", "Small", "session", 600),
    ("grooming", "Bath & blow dry", "Dog", "Medium", "session", 900),
    ("grooming", "Bath & blow dry", "Dog", "Large", "session", 1400),
    ("grooming", "Bath & blow dry", "Dog", "Giant", "session", 2000),
    ("grooming", "Full grooming (bath, haircut, nails, ears)", "Dog", "Small", "session", 1200),
    ("grooming", "Full grooming (bath, haircut, nails, ears)", "Dog", "Medium", "session", 1800),
    ("grooming", "Full grooming (bath, haircut, nails, ears)", "Dog", "Large", "session", 2500),
    ("grooming", "Full grooming (bath, haircut, nails, ears)", "Dog", "Giant", "session", 3500),
    ("grooming", "Nail trimming", "Dog & Cat", "Any", "session", 200),
    ("grooming", "Ear cleaning", "Dog & Cat", "Any", "session", 250),
    ("grooming", "Teeth cleaning", "Dog", "Any", "session", 400),
    ("grooming", "Tick & flea medicated bath", "Dog", "Any", "session", 800),
    ("grooming", "De-shedding treatment", "Dog", "Any", "session", 1000),
    ("grooming", "Cat bath & brush", "Cat", "Any", "session", 1200),
    # Boarding (per night)
    ("boarding", "Dog boarding", "Dog", "Small", "night", 600),
    ("boarding", "Dog boarding", "Dog", "Medium", "night", 800),
    ("boarding", "Dog boarding", "Dog", "Large", "night", 1100),
    ("boarding", "Dog boarding", "Dog", "Giant", "night", 1400),
    ("boarding", "Premium AC suite boarding", "Dog", "Any", "night", 1500),
    ("boarding", "Cat boarding", "Cat", "Any", "night", 500),
    # Day care & pet sitting
    ("daycare", "Dog day care (8 hours)", "Dog", "Small", "day", 600),
    ("daycare", "Dog day care (8 hours)", "Dog", "Medium", "day", 800),
    ("daycare", "Dog day care (8 hours)", "Dog", "Large", "day", 900),
    ("daycare", "Cat day care (8 hours)", "Cat", "Any", "day", 400),
    ("daycare", "Pet sitting at home", "Dog & Cat", "Any", "hour", 300),
    ("daycare", "Full-day care at home (one day)", "Dog & Cat", "Any", "day", 1500),
    ("daycare", "Overnight pet sitting at home", "Dog & Cat", "Any", "night", 1800),
    # Food & meals (per day)
    ("food", "Dry food meals", "Dog", "Small", "day", 100),
    ("food", "Dry food meals", "Dog", "Medium", "day", 180),
    ("food", "Dry food meals", "Dog", "Large", "day", 300),
    ("food", "Dry food meals", "Dog", "Giant", "day", 450),
    ("food", "Home-cooked meals", "Dog", "Small", "day", 150),
    ("food", "Home-cooked meals", "Dog", "Medium", "day", 250),
    ("food", "Home-cooked meals", "Dog", "Large", "day", 400),
    ("food", "Cat food meals", "Cat", "Any", "day", 80),
    # Training (per hour)
    ("training", "Puppy training", "Dog", "Any", "hour", 700),
    ("training", "Basic obedience training", "Dog", "Any", "hour", 800),
    ("training", "Advanced obedience training", "Dog", "Any", "hour", 1200),
    ("training", "Behaviour consultation", "Dog", "Any", "hour", 1000),
    # Vet & health (per visit)
    ("vet", "General consultation", "Dog & Cat", "Any", "visit", 500),
    ("vet", "Vaccination (vaccine included)", "Dog & Cat", "Any", "visit", 700),
    ("vet", "Deworming", "Dog & Cat", "Any", "visit", 250),
    ("vet", "Full health check-up", "Dog & Cat", "Any", "visit", 1200),
    ("vet", "Home vet visit", "Dog & Cat", "Any", "visit", 1200),
    ("vet", "Emergency consultation", "Dog & Cat", "Any", "visit", 1500),
    # Transport (per trip)
    ("transport", "Pet taxi (within city, up to 10 km)", "Dog & Cat", "Any", "trip", 500),
    ("transport", "Pet taxi round trip", "Dog & Cat", "Any", "trip", 900),
]

DESCRIPTIONS = {
    "walking": "Trained walker takes your dog out for exercise and toilet breaks.",
    "grooming": "Professional grooming with pet-safe products.",
    "boarding": "Safe overnight stay with meals, exercise and supervision.",
    "daycare": "Supervised care while you are away.",
    "food": "Fresh water and measured meals for the day.",
    "training": "One-to-one session with a trainer using reward-based methods.",
    "vet": "Veterinary service. Medicines or tests, if needed, are charged extra.",
    "transport": "Safe pick-up and drop for your pet.",
}


class Command(BaseCommand):
    help = "Seed pet services with estimated INR prices"

    def handle(self, *args, **options):
        created = updated = 0
        for category, name, pet_type, size, unit, price in SERVICES:
            _, was_created = PetService.objects.update_or_create(
                name=name,
                pet_type=pet_type,
                size=size,
                defaults={
                    "category": category,
                    "unit": unit,
                    "price": Decimal(price),
                    "description": DESCRIPTIONS[category],
                    "is_active": True,
                },
            )
            created += was_created
            updated += not was_created
        self.stdout.write(self.style.SUCCESS(
            f"Pet services seeded. Created: {created}, updated: {updated}, "
            f"total: {PetService.objects.filter(is_active=True).count()}"
        ))