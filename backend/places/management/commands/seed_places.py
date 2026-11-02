from django.core.management.base import BaseCommand

from places.models import Place

HOTEL_AREAS = ["Indiranagar", "Koramangala", "Whitefield", "MG Road", "Electronic City", "Yelahanka", "Hebbal", "Marathahalli"]
RESTAURANT_AREAS = ["Indiranagar", "Koramangala", "HSR Layout", "Jayanagar", "Whitefield", "Malleshwaram", "Bellandur", "Sarjapur Road"]
CAFE_AREAS = ["Indiranagar", "Koramangala", "HSR Layout", "Jayanagar", "Church Street", "Whitefield"]
PARK_AREAS = ["Indiranagar", "Koramangala", "Whitefield", "Jayanagar"]
RESORT_CITIES = ["Coorg", "Chikmagalur", "Nandi Hills", "Kabini"]


class Command(BaseCommand):
    help = "Seed sample pet-friendly hotels, resorts, restaurants, cafes and parks"

    def add(self, name, category, area="", city="Bangalore", **fields):
        _, created = Place.objects.update_or_create(
            name=name,
            defaults={"category": category, "area": area, "city": city,
                      "is_sample": True, "is_active": True, **fields},
        )
        return created

    def handle(self, *args, **options):
        n = 0
        for i, area in enumerate(HOTEL_AREAS):
            n += self.add(
                f"Sample Pet-friendly Hotel - {area}", "hotel", area,
                price_min=2500 + (i % 3) * 500, price_max=5500 + (i % 3) * 700, price_unit="night",
                pet_fee=500,
                pet_policy="Dogs and cats up to 15 kg welcome. Vaccination certificate required.",
                amenities="Pet bed on request, Walking area, Pet-friendly room service",
            )
        for city in RESORT_CITIES:
            n += self.add(
                f"Sample Pet-friendly Resort - {city}", "resort", "", city,
                price_min=4000, price_max=12000, price_unit="night", pet_fee=1000,
                pet_policy="Pet-friendly cottages. Leash required in common areas.",
                amenities="Open lawns, Nature walks, Pet-friendly cottages",
            )
        for i, area in enumerate(RESTAURANT_AREAS):
            n += self.add(
                f"Sample Pet-friendly Restaurant - {area}", "restaurant", area,
                price_min=800 + (i % 3) * 200, price_max=1800 + (i % 3) * 300, price_unit="for two",
                pet_policy="Pets welcome in outdoor seating. Leash required.",
                amenities="Outdoor seating, Water bowls",
            )
        for i, area in enumerate(CAFE_AREAS):
            n += self.add(
                f"Sample Pet-friendly Cafe - {area}", "cafe", area,
                price_min=400 + (i % 3) * 100, price_max=900 + (i % 3) * 150, price_unit="for two",
                pet_policy="Pet-friendly patio. Leash required.",
                amenities="Patio seating, Water bowls, Pet treats on menu",
            )
        for area in PARK_AREAS:
            n += self.add(
                f"Sample Dog Park - {area}", "park", area,
                price_min=0, price_max=0, price_unit="entry",
                pet_policy="Dogs welcome. Clean up after your pet and follow park timings.",
                amenities="Open space, Walking track",
            )
        self.stdout.write(self.style.SUCCESS(f"Places seeded. New: {n}, total: {Place.objects.count()}"))