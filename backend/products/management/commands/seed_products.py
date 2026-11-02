from decimal import Decimal

from django.core.management.base import BaseCommand

from products.models import Product

# (category, name, pet_type, pack, price in INR). Estimates; edit in /admin.
PRODUCTS = [
    ("food", "Puppy dry food", "Dog", "1 kg", 450),
    ("food", "Adult dog dry food", "Dog", "3 kg", 1100),
    ("food", "Adult dog dry food (large breed)", "Dog", "10 kg", 2800),
    ("food", "Senior dog food", "Dog", "3 kg", 1250),
    ("food", "Grain-free dog food", "Dog", "2 kg", 1800),
    ("food", "Wet dog food pouch", "Dog", "100 g", 65),
    ("food", "Kitten dry food", "Cat", "1 kg", 550),
    ("food", "Adult cat dry food", "Cat", "1.2 kg", 650),
    ("food", "Wet cat food (tuna)", "Cat", "85 g", 50),
    ("food", "Rabbit pellets", "Small pets", "1 kg", 350),
    ("food", "Timothy hay", "Small pets", "1 kg", 400),
    ("food", "Hamster seed mix", "Small pets", "500 g", 250),
    ("food", "Guinea pig food (with vitamin C)", "Small pets", "1 kg", 450),
    ("food", "Budgie seed mix", "Birds", "1 kg", 250),
    ("food", "Parrot nut & seed mix", "Birds", "1 kg", 500),
    ("food", "Cockatiel seed mix", "Birds", "1 kg", 350),
    ("food", "Goldfish flakes", "Fish", "100 g", 180),
    ("food", "Betta pellets", "Fish", "50 g", 150),
    ("food", "Tropical fish flakes", "Fish", "100 g", 200),
    ("food", "Tortoise pellets", "Reptiles", "500 g", 450),
    ("treats", "Chicken jerky treats", "Dog", "200 g", 300),
    ("treats", "Dental chew sticks", "Dog", "7 pack", 350),
    ("treats", "Training treats", "Dog", "150 g", 250),
    ("treats", "Creamy cat treats", "Cat", "4 pack", 180),
    ("treats", "Catnip treats", "Cat", "60 g", 200),
    ("treats", "Rabbit chew sticks", "Small pets", "100 g", 220),
    ("treats", "Millet spray", "Birds", "100 g", 150),
    ("toys", "Rubber chew toy", "Dog", "Medium", 250),
    ("toys", "Squeaky plush toy", "Dog", "1 pc", 200),
    ("toys", "Rope tug toy", "Dog", "1 pc", 220),
    ("toys", "Tennis fetch balls", "Dog", "3 pack", 300),
    ("toys", "Treat puzzle toy", "Dog", "1 pc", 600),
    ("toys", "Feather wand", "Cat", "1 pc", 180),
    ("toys", "Catnip mice", "Cat", "3 pack", 200),
    ("toys", "Play tunnel", "Cat", "1 pc", 700),
    ("toys", "Scratching post", "Cat", "1 pc", 900),
    ("toys", "Silent hamster wheel", "Small pets", "1 pc", 450),
    ("toys", "Bird swing & bell", "Birds", "1 pc", 180),
    ("toys", "Bird foraging toy", "Birds", "1 pc", 350),
    ("bedding", "Dog bed", "Dog", "Medium", 1200),
    ("bedding", "Dog bed", "Dog", "Large", 1800),
    ("bedding", "Orthopedic dog mattress", "Dog", "Large", 3500),
    ("bedding", "Cat cushion bed", "Cat", "1 pc", 800),
    ("bedding", "Cat cave bed", "Cat", "1 pc", 1100),
    ("bedding", "Paper bedding", "Small pets", "10 L", 450),
    ("grooming", "Herbal dog shampoo", "Dog", "200 ml", 350),
    ("grooming", "Cat shampoo", "Cat", "200 ml", 350),
    ("grooming", "Slicker brush", "Dog & Cat", "1 pc", 300),
    ("grooming", "Nail clipper", "Dog & Cat", "1 pc", 250),
    ("grooming", "De-shedding tool", "Dog", "1 pc", 600),
    ("grooming", "Ear cleaning solution", "Dog & Cat", "100 ml", 300),
    ("grooming", "Toothbrush & paste kit", "Dog & Cat", "1 kit", 300),
    ("health", "Pet first-aid kit", "All", "1 kit", 900),
    ("health", "Grooming wet wipes", "Dog & Cat", "80 wipes", 250),
    ("health", "Poop bags", "Dog", "120 bags", 200),
    ("accessories", "Adjustable dog collar", "Dog", "Medium", 300),
    ("accessories", "Dog leash", "Dog", "1.5 m", 350),
    ("accessories", "No-pull harness", "Dog", "Medium", 700),
    ("accessories", "Retractable leash", "Dog", "5 m", 900),
    ("accessories", "Cat collar with bell", "Cat", "1 pc", 150),
    ("accessories", "Cat harness & leash", "Cat", "1 set", 500),
    ("accessories", "Stainless steel bowl", "Dog & Cat", "1 pc", 300),
    ("accessories", "Automatic feeder", "Dog & Cat", "1 pc", 2500),
    ("accessories", "Water fountain", "Cat", "1 pc", 1800),
    ("travel", "Pet carrier", "Dog & Cat", "Small", 1500),
    ("travel", "Car seat cover", "Dog", "1 pc", 1500),
    ("travel", "Travel water bottle", "Dog & Cat", "1 pc", 400),
    ("aquarium", "Aquarium tank", "Fish", "20 L", 1200),
    ("aquarium", "Air pump", "Fish", "1 pc", 450),
    ("aquarium", "Internal filter", "Fish", "1 pc", 700),
    ("aquarium", "Aquarium heater", "Fish", "100 W", 600),
    ("aquarium", "LED aquarium light", "Fish", "1 pc", 800),
    ("aquarium", "Water conditioner", "Fish", "100 ml", 180),
    ("aquarium", "Aquarium gravel", "Fish", "1 kg", 150),
    ("aquarium", "Artificial plants", "Fish", "1 set", 250),
    ("cage", "Bird cage", "Birds", "Medium", 2200),
    ("cage", "Hamster cage", "Small pets", "1 pc", 1500),
    ("cage", "Rabbit hutch", "Small pets", "1 pc", 4500),
    ("cage", "Tortoise enclosure", "Reptiles", "1 pc", 5000),
    ("cage", "UVB lamp", "Reptiles", "1 pc", 1800),
    ("litter", "Clumping cat litter", "Cat", "5 kg", 450),
    ("litter", "Litter tray", "Cat", "1 pc", 400),
    ("litter", "Litter scoop", "Cat", "1 pc", 120),
    ("litter", "Stain & odour remover", "All", "500 ml", 350),
]

DESCRIPTIONS = {
    "food": "Complete, balanced food. Choose the right life stage and size for your pet.",
    "treats": "Occasional treats and rewards. Give in moderation.",
    "toys": "Play and enrichment. Supervise play and replace worn toys.",
    "bedding": "A comfortable, clean resting place.",
    "grooming": "Keeps coat, skin, nails and teeth healthy.",
    "health": "Everyday hygiene and first-aid supplies.",
    "accessories": "Walking, feeding and daily-use accessories.",
    "travel": "Safe and comfortable travel for your pet.",
    "aquarium": "Equipment for a healthy, filtered aquarium.",
    "cage": "Safe housing with room to move.",
    "litter": "Keeps the home clean and odour-free.",
}


class Command(BaseCommand):
    help = "Seed pet products with estimated INR prices"

    def handle(self, *args, **options):
        created = updated = 0
        for category, name, pet_type, pack, price in PRODUCTS:
            _, was_created = Product.objects.update_or_create(
                name=name, pet_type=pet_type, pack=pack,
                defaults={"category": category, "price": Decimal(price),
                          "description": DESCRIPTIONS[category], "in_stock": True, "is_active": True},
            )
            created += was_created
            updated += not was_created
        self.stdout.write(self.style.SUCCESS(
            f"Products seeded. Created: {created}, updated: {updated}, "
            f"total: {Product.objects.filter(is_active=True).count()}"))