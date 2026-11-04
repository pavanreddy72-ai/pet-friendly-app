
import re

from django.core.management.base import BaseCommand

from products.models import Product


CURATED = {
    "food": [
        "Chicken Puppy Food",
        "Adult Chicken Food",
        "Senior Dog Food",
        "Large Breed Food",
        "Small Breed Food",
        "Grain Free Food",
        "Lamb Dog Food",
        "Salmon Dog Food",
        "Wet Dog Food",
        "Kitten Food",
        "Adult Cat Food",
        "Senior Cat Food",
        "Persian Cat Food",
        "Rabbit Timothy Hay",
        "Goldfish Food",
        "Guinea Pig Food",
        "Hamster Complete Food",
        "Budgie Seed Mix",
        "Rabbit Pellets",
        "Hairball Control Food",
        "Chicken Cat Food",
        "Salmon Cat Food",
        "Urinary Care Food",
        "Puppy Dry Food",
        "Adult Dog Dry Food",
    ],
    "treats": [
        "Chicken Training Bites",
        "Beef Dog Treats",
        "Salmon Dog Treats",
        "Dental Chew Sticks",
        "Lamb Dog Biscuits",
        "Peanut Butter Treats",
        "Duck Dog Jerky",
        "Sweet Potato Chews",
        "Apple Dog Biscuits",
        "Carrot Dog Treats",
        "Crunchy Cat Treats",
        "Tuna Cat Treats",
        "Catnip Treats",
        "Chicken Cat Treats",
        "Bird Millet Spray",
    ],
    "toys": [
        "Rope Chew Toy",
        "Rubber Fetch Ball",
        "Dog Puzzle Toy",
        "Squeaky Dog Toy",
        "Dog Tug Toy",
        "Dog Frisbee",
        "Dog Treat Dispenser",
        "Dog Chew Ring",
        "Dog Plush Toy",
        "Dog Interactive Ball",
        "Interactive Cat Ball",
        "Cat Feather Wand",
        "Catnip Mouse Toy",
        "Cat Scratching Toy",
        "Cat Puzzle Feeder",
        "Cat Tunnel Toy",
        "Cat Bell Ball",
        "Rabbit Chew Toy",
        "Cat Activity Track",
        "Bird Hanging Swing",
    ],
    "bedding": [
        "Orthopedic Dog Bed",
        "Puppy Sleeping Mat",
        "Large Dog Cushion",
        "Waterproof Dog Mattress",
        "Travel Dog Blanket",
        "Memory Foam Dog Bed",
        "Round Dog Bed",
        "Cooling Dog Mat",
        "Soft Cat Sleeping Bed",
        "Cat Window Hammock",
        "Cat Cave Bed",
        "Kitten Sleeping Cushion",
        "Cat Blanket",
        "Cat Donut Bed",
        "Rabbit Paper Bedding",
    ],
    "grooming": [
        "Dog Grooming Brush",
        "Dog Deshedding Comb",
        "Dog Bath Shampoo",
        "Dog Nail Clipper",
        "Dog Slicker Brush",
        "Dog Grooming Gloves",
        "Dog Fur Detangler",
        "Dog Bath Wipes",
        "Dog Ear Cleaning Wipes",
        "Cat Grooming Brush",
        "Cat Deshedding Comb",
        "Cat Bath Wipes",
        "Cat Nail Clipper",
        "Cat Slicker Brush",
        "Cat Grooming Gloves",
        "Cat Shampoo",
        "Rabbit Grooming Comb",
        "Guinea Pig Grooming Brush",
        "Bird Feather Care Spray",
        "Pet Grooming Kit",
    ],
    "health": [
        "Pet First Aid Kit",
        "Dog Dental Care Kit",
        "Dog Paw Protection Balm",
        "Dog Skin Care Shampoo",
        "Dog Ear Care Kit",
        "Dog Recovery Collar",
        "Dog Toothbrush",
        "Dog Dental Wipes",
        "Cat Dental Care Kit",
        "Cat Hairball Support Paste",
        "Cat Recovery Collar",
        "Cat Toothbrush",
        "Pet Wound Dressing Kit",
        "Pet Tick Removal Tool",
        "Pet Digital Thermometer",
    ],
    "accessories": [
        "Adjustable Dog Collar",
        "Reflective Dog Collar",
        "Dog Walking Harness",
        "Dog Leash",
        "Dog ID Tag",
        "Dog Bandana",
        "Dog Raincoat",
        "Dog Winter Sweater",
        "Dog Feeding Bowl",
        "Dog Water Bowl",
        "Cat Safety Collar",
        "Cat Breakaway Collar",
        "Cat Harness",
        "Cat ID Tag",
        "Cat Bell Collar",
        "Cat Feeding Bowl",
        "Cat Water Fountain",
        "Rabbit Harness",
        "Bird Perch",
        "Pet Feeding Mat",
    ],
    "travel": [
        "Pet Travel Water Bottle",
        "Dog Car Seat Cover",
        "Dog Travel Carrier",
        "Dog Travel Bowl",
        "Dog Car Safety Belt",
        "Dog Travel Backpack",
        "Dog Portable Kennel",
        "Dog Travel Blanket",
        "Dog Outdoor Tent",
        "Cat Travel Backpack",
        "Cat Hard Carrier",
        "Cat Travel Cushion",
        "Cat Travel Blanket",
        "Rabbit Travel Carrier",
        "Bird Travel Cage",
    ],
    "aquarium": [
        "Aquarium Internal Filter",
        "Aquarium External Filter",
        "Aquarium Air Pump",
        "Aquarium LED Light",
        "Aquarium Heater",
        "Fish Flake Food",
        "Tropical Fish Pellets",
        "Aquarium Gravel",
        "Aquarium Cleaning Siphon",
        "Aquarium Fish Net",
    ],
    "cage": [
        "Large Bird Cage",
        "Small Bird Cage",
        "Parrot Play Stand",
        "Budgie Cage Perch",
        "Bird Cage Food Cup",
        "Cockatiel Cage",
        "Lovebird Cage",
        "Finch Flight Cage",
        "Canary Cage",
        "Rabbit Indoor Cage",
    ],
    "litter": [
        "Clumping Cat Litter",
        "Non Clumping Cat Litter",
        "Silica Cat Litter",
        "Natural Wood Cat Litter",
        "Tofu Cat Litter",
        "Unscented Cat Litter",
        "Cat Litter Tray",
        "Covered Cat Litter Box",
        "Cat Litter Scoop",
        "Cat Litter Mat",
        "Cat Litter Disposal Bags",
        "Corn Cat Litter",
        "Paper Cat Litter",
        "Rabbit Paper Litter",
        "Small Pet Litter Tray",
    ],
}


def normalize(name):
    return re.sub(
        r"\s*-\s*(Small|Large)\s+Pack$",
        "",
        name.strip(),
        flags=re.IGNORECASE,
    ).casefold()


class Command(BaseCommand):
    help = "Keep a curated selection of 180 pet product groups."

    def handle(self, *args, **options):
        expected = 180
        actual = sum(len(items) for items in CURATED.values())

        if actual != expected:
            self.stderr.write(
                self.style.ERROR(
                    f"Expected {expected} products, found {actual}."
                )
            )
            return

        selected = {
            (category, normalize(name))
            for category, names in CURATED.items()
            for name in names
        }

        products = list(Product.objects.filter(is_active=True))
        matched = set()

        for product in products:
            category = (product.category or "").casefold()
            base_name = normalize(product.name)

            if (category, base_name) in selected:
                matched.add((category, base_name))

        missing = selected - matched

        if missing:
            self.stderr.write(
                self.style.ERROR(
                    f"{len(missing)} curated products were not found."
                )
            )
            for category, name in sorted(missing):
                self.stderr.write(f"Missing: {category} | {name}")

            self.stderr.write(
                "No products were changed. Check missing names first."
            )
            return

        # Only deactivate products after confirming every selection exists.
        Product.objects.filter(is_active=True).update(is_active=False)

        kept = 0
        for product in products:
            key = (
                (product.category or "").casefold(),
                normalize(product.name),
            )
            if key in selected:
                product.is_active = True
                product.save(update_fields=["is_active"])
                kept += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Curated successfully. Active product records: {kept}"
            )
        )

        for category in CURATED:
            count = Product.objects.filter(
                category__iexact=category,
                is_active=True,
            ).count()
            self.stdout.write(f"{category}: {count}")
