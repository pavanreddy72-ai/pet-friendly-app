
import hashlib
import re
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Product


# Each category has 25 products.
# Each product gets two pack variants: Small and Large.
# Total: 11 categories x 25 products x 2 variants = 550.

DATA = {
    "food": {
        "pet": "Dog",
        "price": 450,
        "items": [
            "Chicken Puppy Food", "Adult Chicken Food", "Senior Dog Food",
            "Large Breed Food", "Small Breed Food", "Grain Free Food",
            "Lamb Dog Food", "Salmon Dog Food", "Sensitive Stomach Food",
            "Wet Dog Food", "Kitten Food", "Adult Cat Food",
            "Senior Cat Food", "Persian Cat Food", "Hairball Control Food",
            "Urinary Care Food", "Salmon Cat Food", "Chicken Cat Food",
            "Rabbit Timothy Hay", "Rabbit Pellets", "Guinea Pig Food",
            "Hamster Complete Food", "Chinchilla Pellets",
            "Budgie Seed Mix", "Goldfish Food",
        ],
    },
    "treats": {
        "pet": "Dog",
        "price": 200,
        "items": [
            "Chicken Training Bites", "Beef Dog Treats", "Salmon Dog Treats",
            "Dental Chew Sticks", "Lamb Dog Biscuits", "Peanut Butter Treats",
            "Duck Dog Jerky", "Sweet Potato Chews", "Apple Dog Biscuits",
            "Carrot Dog Treats", "Crunchy Cat Treats", "Tuna Cat Treats",
            "Salmon Cat Bites", "Catnip Treats", "Creamy Cat Snacks",
            "Chicken Cat Treats", "Dental Cat Treats", "Duck Cat Treats",
            "Rabbit Apple Treats", "Carrot Rabbit Snacks",
            "Guinea Pig Herb Treats", "Hamster Fruit Treats",
            "Chinchilla Rosehip Treats", "Bird Millet Spray",
            "Betta Fish Treats",
        ],
    },
    "toys": {
        "pet": "Dog",
        "price": 180,
        "items": [
            "Rope Chew Toy", "Rubber Fetch Ball", "Dog Puzzle Toy",
            "Squeaky Dog Toy", "Dog Tug Toy", "Dog Frisbee",
            "Dog Treat Dispenser", "Dog Chew Ring", "Dog Plush Toy",
            "Dog Interactive Ball", "Interactive Cat Ball",
            "Cat Feather Wand", "Catnip Mouse Toy", "Cat Scratching Toy",
            "Cat Puzzle Feeder", "Cat Tunnel Toy", "Cat Bell Ball",
            "Cat Plush Toy", "Cat Activity Track", "Cat Scratching Board",
            "Rabbit Play Tunnel", "Rabbit Chew Toy",
            "Guinea Pig Play Tunnel", "Hamster Exercise Wheel",
            "Bird Hanging Swing",
        ],
    },
    "bedding": {
        "pet": "Dog",
        "price": 350,
        "items": [
            "Orthopedic Dog Bed", "Puppy Sleeping Mat", "Large Dog Cushion",
            "Waterproof Dog Mattress", "Travel Dog Blanket",
            "Memory Foam Dog Bed", "Round Dog Bed", "Cooling Dog Mat",
            "Washable Dog Mattress", "Dog Sofa Bed",
            "Soft Cat Sleeping Bed", "Cat Window Hammock", "Cat Cave Bed",
            "Kitten Sleeping Cushion", "Cat Blanket", "Cat Donut Bed",
            "Heated Cat Mat", "Cat Window Bed", "Washable Cat Cushion",
            "Large Cat Bed", "Rabbit Paper Bedding", "Rabbit Hay Bedding",
            "Guinea Pig Fleece Bedding", "Hamster Paper Bedding",
            "Bird Cage Bedding",
        ],
    },
    "grooming": {
        "pet": "Dog",
        "price": 180,
        "items": [
            "Dog Grooming Brush", "Dog Deshedding Comb", "Dog Bath Shampoo",
            "Dog Paw Cleaning Foam", "Dog Nail Clipper", "Dog Slicker Brush",
            "Dog Grooming Gloves", "Dog Fur Detangler", "Dog Bath Wipes",
            "Dog Ear Cleaning Wipes", "Cat Grooming Brush",
            "Cat Deshedding Comb", "Cat Bath Wipes", "Cat Nail Clipper",
            "Cat Fur Detangling Spray", "Cat Slicker Brush",
            "Cat Grooming Gloves", "Cat Shampoo", "Cat Ear Cleaning Wipes",
            "Cat Hair Remover", "Rabbit Grooming Comb",
            "Guinea Pig Grooming Brush", "Hamster Soft Brush",
            "Bird Feather Care Spray", "Pet Grooming Kit",
        ],
    },
    "health": {
        "pet": "Dog",
        "price": 180,
        "items": [
            "Pet First Aid Kit", "Dog Dental Care Kit",
            "Dog Paw Protection Balm", "Dog Skin Care Shampoo",
            "Dog Ear Care Kit", "Dog Recovery Collar", "Dog Toothbrush",
            "Dog Dental Wipes", "Cat Dental Care Kit",
            "Cat Hairball Support Paste", "Cat Skin Care Wipes",
            "Cat Recovery Collar", "Cat Toothbrush", "Cat Dental Wipes",
            "Pet Wound Dressing Kit", "Pet Tick Removal Tool",
            "Pet Digital Thermometer", "Pet Medicine Organizer",
            "Rabbit Health Care Kit", "Guinea Pig Vitamin C Supplement",
            "Hamster Health Care Kit", "Bird Mineral Block",
            "Bird Calcium Supplement", "Fish Water Test Kit",
            "Aquarium Water Conditioner",
        ],
    },
    "accessories": {
        "pet": "Dog",
        "price": 120,
        "items": [
            "Adjustable Dog Collar", "Reflective Dog Collar",
            "Dog Walking Harness", "Dog Leash", "Dog ID Tag",
            "Dog Bandana", "Dog Raincoat", "Dog Winter Sweater",
            "Dog Feeding Bowl", "Dog Water Bowl", "Cat Safety Collar",
            "Cat Breakaway Collar", "Cat Harness", "Cat ID Tag",
            "Cat Bell Collar", "Cat Feeding Bowl", "Cat Water Fountain",
            "Cat Window Perch", "Rabbit Harness", "Rabbit Feeding Bowl",
            "Guinea Pig Water Bottle", "Hamster Food Bowl",
            "Bird Perch", "Parrot Stand", "Pet Feeding Mat",
        ],
    },
    "travel": {
        "pet": "Dog",
        "price": 200,
        "items": [
            "Pet Travel Water Bottle", "Dog Car Seat Cover",
            "Dog Travel Carrier", "Dog Travel Bowl", "Dog Car Safety Belt",
            "Dog Travel Backpack", "Dog Portable Kennel",
            "Dog Travel Blanket", "Dog Outdoor Tent",
            "Dog Travel Food Container", "Cat Travel Backpack",
            "Cat Hard Carrier", "Cat Travel Cushion",
            "Cat Car Safety Carrier", "Cat Travel Blanket",
            "Cat Portable Kennel", "Cat Travel Bag", "Cat Travel Bowl",
            "Rabbit Travel Carrier", "Rabbit Travel Box",
            "Guinea Pig Travel Box", "Hamster Travel Container",
            "Bird Travel Cage", "Parrot Travel Carrier", "Pet Travel Kit",
        ],
    },
    "aquarium": {
        "pet": "Fish",
        "price": 100,
        "items": [
            "Aquarium Internal Filter", "Aquarium External Filter",
            "Aquarium Air Pump", "Aquarium LED Light", "Aquarium Heater",
            "Fish Flake Food", "Tropical Fish Pellets",
            "Goldfish Food Pellets", "Aquarium Gravel",
            "Aquarium Decorative Plants", "Aquarium Cleaning Siphon",
            "Aquarium Water Conditioner", "Aquarium Thermometer",
            "Fish Breeding Box", "Aquarium Sponge Filter",
            "Aquarium Air Stone", "Fish Tank Background",
            "Aquarium Cleaning Brush", "Aquarium Fish Net",
            "Aquarium Starter Kit", "Aquarium Canister Filter",
            "Aquarium UV Sterilizer", "Aquarium CO2 Kit",
            "Aquarium Auto Feeder", "Aquarium Water Test Kit",
        ],
    },
    "cage": {
        "pet": "Bird",
        "price": 180,
        "items": [
            "Large Bird Cage", "Small Bird Cage", "Parrot Play Stand",
            "Budgie Cage Perch", "Bird Cage Food Cup", "Cockatiel Cage",
            "Lovebird Cage", "Finch Flight Cage", "Canary Cage",
            "Bird Cage Cover", "Rabbit Indoor Cage", "Rabbit Outdoor Hutch",
            "Rabbit Multi Level Cage", "Rabbit Exercise Pen",
            "Rabbit Cage Tray", "Guinea Pig Habitat",
            "Guinea Pig Cage Liner", "Guinea Pig Playpen",
            "Hamster Glass Habitat", "Hamster Modular Cage",
            "Hamster Exercise Wheel", "Hamster Cage Tunnel",
            "Chinchilla Cage", "Pet Rat Multi Level Cage",
            "Small Animal Playpen",
        ],
    },
    "litter": {
        "pet": "Cat",
        "price": 120,
        "items": [
            "Clumping Cat Litter", "Non Clumping Cat Litter",
            "Silica Cat Litter", "Natural Wood Cat Litter",
            "Tofu Cat Litter", "Unscented Cat Litter",
            "Lavender Cat Litter", "Multi Cat Litter", "Cat Litter Tray",
            "Covered Cat Litter Box", "Cat Litter Scoop", "Cat Litter Mat",
            "Cat Litter Disposal Bags", "Activated Charcoal Cat Litter",
            "Corn Cat Litter", "Paper Cat Litter",
            "Fast Clumping Cat Litter", "Low Dust Cat Litter",
            "Odour Control Cat Litter", "Large Cat Litter Tray",
            "Rabbit Paper Litter", "Rabbit Wood Pellet Litter",
            "Guinea Pig Paper Litter", "Hamster Paper Litter",
            "Small Pet Litter Tray",
        ],
    },
}


DESCRIPTIONS = {
    "food": "Demonstration pet food listing. Check ingredients, life stage and feeding guidance.",
    "treats": "Pet treat demonstration listing. Offer in moderation.",
    "toys": "Pet enrichment toy. Supervise play and replace damaged items.",
    "bedding": "Pet bedding product. Keep clean and choose the correct size.",
    "grooming": "Pet grooming accessory. Follow safe grooming instructions.",
    "health": "Pet care accessory. Not a medicine or substitute for veterinary advice.",
    "accessories": "Everyday pet accessory for home, feeding or walking.",
    "travel": "Pet travel accessory. Check size and safety before travelling.",
    "aquarium": "Aquarium equipment. Check tank compatibility before use.",
    "cage": "Pet housing accessory. Ensure sufficient space and ventilation.",
    "litter": "Pet hygiene product. Choose safe material suitable for your animal.",
}


PET_KEYWORDS = {
    "dog": "dog",
    "cat": "cat",
    "rabbit": "rabbit",
    "guinea pig": "guinea-pig",
    "hamster": "hamster",
    "chinchilla": "chinchilla",
    "bird": "bird",
    "fish": "fish",
    "tortoise": "tortoise",
    "rat": "rat",
}


def get_product_image(name, pet_type):
    """
    Create a stable, product-specific real-photo search URL.
    Both pack sizes of the same product share one image.
    """

    base_name = re.sub(
        r"\s*-\s*(Small|Large) Pack$",
        "",
        name,
        flags=re.IGNORECASE,
    )

    animal = PET_KEYWORDS.get(pet_type.lower(), "pet")

    words = re.findall(r"[a-z0-9]+", base_name.lower())

    ignored = {
        "dog", "cat", "rabbit", "guinea", "pig", "hamster",
        "chinchilla", "bird", "fish", "pet", "small", "large",
        "for", "and", "the", "with",
    }

    product_words = [
        word for word in words
        if word not in ignored
    ]

    tags = ",".join([animal] + product_words[:2])

    image_lock = int(
        hashlib.sha256(
            base_name.lower().encode("utf-8")
        ).hexdigest()[:8],
        16,
    )

    return (
        f"https://loremflickr.com/700/500/{tags}"
        f"?lock={image_lock}"
    )


class Command(BaseCommand):
    help = "Seed 550 realistic demonstration pet products"

    @transaction.atomic
    def handle(self, *args, **options):
        created = 0
        updated = 0

        for category, config in DATA.items():
            items = config["items"]

            if len(items) != 25:
                raise ValueError(
                    f"{category} must contain 25 products; "
                    f"found {len(items)}"
                )

            for index, name in enumerate(items):
                # Use the category's default pet type unless the
                # product name clearly identifies another animal.
                pet_type = config["pet"]

                animal_overrides = [
                    ("Guinea Pig", "Guinea pig"),
                    ("Chinchilla", "Chinchilla"),
                    ("Hamster", "Hamster"),
                    ("Rabbit", "Rabbit"),
                    ("Budgie", "Bird"),
                    ("Parrot", "Bird"),
                    ("Cockatiel", "Bird"),
                    ("Lovebird", "Bird"),
                    ("Finch", "Bird"),
                    ("Canary", "Bird"),
                    ("Bird", "Bird"),
                    ("Goldfish", "Fish"),
                    ("Aquarium", "Fish"),
                    ("Fish", "Fish"),
                    ("Cat", "Cat"),
                    ("Kitten", "Cat"),
                    ("Dog", "Dog"),
                ]

                for keyword, animal in animal_overrides:
                    if keyword.lower() in name.lower():
                        pet_type = animal
                        break

                # Two pack variants per base product.
                variants = [
                    ("Small Pack", "Small", Decimal("1.00")),
                    ("Large Pack", "Large", Decimal("1.80")),
                ]

                image_url = get_product_image(name, pet_type)

                for variant, pack, multiplier in variants:
                    product_name = f"{name} - {variant}"

                    price = (
                        Decimal(config["price"] + index * 10)
                        * multiplier
                    ).quantize(Decimal("0.01"))

                    _, was_created = Product.objects.update_or_create(
                        name=product_name,
                        pet_type=pet_type,
                        pack=pack,
                        defaults={
                            "category": category,
                            "price": price,
                            "description": DESCRIPTIONS[category],
                            "image_url": image_url,
                            "in_stock": True,
                            "is_active": True,
                        },
                    )

                    if was_created:
                        created += 1
                    else:
                        updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. Created: {created}, "
                f"updated: {updated}, "
                f"active total: "
                f"{Product.objects.filter(is_active=True).count()}"
            )
        )

        self.stdout.write("Category totals:")

        for category in DATA:
            count = Product.objects.filter(
                category=category,
                is_active=True,
            ).count()

            self.stdout.write(f"  {category}: {count}")
