from django.core.management.base import BaseCommand

from vets.models import Hospital, Medication

AREAS = [
    "Koramangala", "Indiranagar", "HSR Layout", "BTM Layout", "Jayanagar",
    "JP Nagar", "Banashankari", "Malleshwaram", "Rajajinagar", "Hebbal",
    "Yelahanka", "Whitefield", "Marathahalli", "Bellandur", "Sarjapur Road",
    "Electronic City", "KR Puram", "Kengeri", "Basavanagudi", "Bannerghatta Road",
]

# kind, services, fee_min, fee_max, hours, emergency
KINDS = [
    ("Veterinary Clinic", "General consultation, Vaccination, Deworming, Grooming, Pharmacy", 400, 700, "9 AM - 8 PM", False),
    ("Pet Hospital", "General consultation, Vaccination, Surgery, X-ray & scan, Dental care, Pharmacy", 600, 1000, "8 AM - 10 PM", False),
    ("24x7 Emergency Pet Hospital", "Emergency care, Surgery, ICU, X-ray & scan, Pharmacy, Pet ambulance", 900, 1500, "Open 24 hours", True),
]

# (name, category, pet_type, form, used_for, price_min, price_max, prescription, notes)
MEDICATIONS = [
    ("Deworming tablets", "deworming", "Dog & Cat", "Tablet", "Treats common intestinal worms", 50, 250, False, "Dose depends on body weight; follow the schedule your vet advises."),
    ("Deworming syrup (puppies & kittens)", "deworming", "Dog & Cat", "Syrup", "Gentle deworming for young pets", 80, 200, False, "Use only products made for puppies/kittens."),
    ("Tick & flea spot-on", "parasite", "Dog", "Spot-on liquid", "Kills ticks and fleas on the skin", 350, 900, False, "Pick the right weight band. Never use dog products on cats."),
    ("Tick & flea spot-on for cats", "parasite", "Cat", "Spot-on liquid", "Kills ticks and fleas on cats", 350, 900, False, "Use only cat-labelled products."),
    ("Tick & flea chewable", "parasite", "Dog", "Chewable tablet", "Monthly tick and flea control", 500, 1500, False, "Ask your vet which option suits your dog."),
    ("Anti-tick collar", "parasite", "Dog", "Collar", "Long-lasting tick protection", 300, 900, False, "Check the neck for irritation."),
    ("Medicated shampoo", "skin", "Dog", "Shampoo", "Itchy or sensitive skin", 250, 600, False, "Do not use human shampoo."),
    ("Antifungal skin ointment", "skin", "Dog & Cat", "Ointment", "Fungal patches such as ringworm", 150, 400, True, "Get a vet diagnosis first."),
    ("Antiseptic wound spray", "wound", "Dog & Cat", "Spray", "Cleans minor cuts and scrapes", 150, 400, False, "Deep or bleeding wounds need a vet."),
    ("Ear cleaner drops", "ear", "Dog & Cat", "Drops", "Routine ear cleaning", 200, 450, False, "Never push anything deep into the ear."),
    ("Ear infection drops", "ear", "Dog & Cat", "Drops", "Ear infections", 200, 600, True, "Needs a vet examination."),
    ("Eye cleaning drops", "eye", "Dog & Cat", "Drops", "Cleans discharge and tear stains", 150, 400, False, "Redness or swelling needs a vet."),
    ("Multivitamin syrup", "supplement", "Dog & Cat", "Syrup", "General nutrition support", 200, 600, False, "Not needed on a complete diet unless advised."),
    ("Calcium supplement", "supplement", "Dog", "Tablet or syrup", "Bone support during growth", 200, 500, False, "Over-supplementing can harm growing puppies."),
    ("Joint support (glucosamine)", "supplement", "Dog", "Tablet", "Joint comfort in older or large dogs", 500, 1500, False, "Ask your vet about duration."),
    ("Probiotic powder", "digestive", "Dog & Cat", "Powder", "Supports gut health", 250, 700, False, "Mix with food."),
    ("Electrolyte powder (pet ORS)", "digestive", "Dog & Cat", "Powder", "Mild dehydration support on the way to the vet", 100, 250, False, "Not a replacement for vet care in vomiting or diarrhoea."),
    ("Small pet gut care paste", "digestive", "Small pets", "Paste", "Digestive support for rabbits and guinea pigs", 300, 700, False, "Not eating for 12+ hours is an emergency in rabbits."),
    ("Bird vitamin drops", "supplement", "Birds", "Drops", "Vitamin support in water", 120, 350, False, "Follow the label for dilution."),
    ("Antibiotics (as prescribed)", "prescription", "Dog & Cat", "Tablet or syrup", "Bacterial infections", 150, 800, True, "Never use leftover or human antibiotics. Finish the course."),
    ("Pain relief / anti-inflammatory", "prescription", "Dog & Cat", "Tablet", "Pain and swelling after injury or surgery", 150, 700, True, "Human painkillers can be toxic to pets."),
    ("Anti-allergy medicine", "prescription", "Dog", "Tablet", "Allergic itching", 200, 900, True, "Find the cause with your vet."),
    ("Anti-nausea / anti-vomiting", "prescription", "Dog & Cat", "Tablet or injection", "Vomiting under vet direction", 150, 600, True, "Repeated vomiting needs a vet visit."),
    ("Rabies vaccine", "vaccine", "Dog & Cat", "Injection", "Core vaccine; often needed for boarding and travel", 300, 600, True, "Given by a vet; keep the vaccination card."),
    ("DHPPi (multi-disease) vaccine", "vaccine", "Dog", "Injection", "Distemper, hepatitis, parvovirus and more", 600, 1200, True, "Puppies need a series of doses."),
    ("Feline core vaccine", "vaccine", "Cat", "Injection", "Cat flu and panleukopenia", 700, 1400, True, "Given by a vet."),
    ("Aquarium disease treatment", "aquarium", "Fish", "Liquid", "Common fungal or bacterial fish ailments", 150, 500, False, "Remove carbon from the filter while treating."),
]


class Command(BaseCommand):
    help = "Seed sample vet hospitals and medication information"

    def handle(self, *args, **options):
        h_new = 0
        for i, area in enumerate(AREAS):
            kind, services, fmin, fmax, hours, emergency = KINDS[i % len(KINDS)]
            _, created = Hospital.objects.update_or_create(
                name=f"Sample {kind} - {area}",
                defaults={
                    "area": area, "city": "Bangalore", "services": services,
                    "pet_types": "Dogs, Cats, Small pets" if i % 3 else "Dogs, Cats",
                    "open_hours": hours, "emergency_24x7": emergency,
                    "home_visits": kind == KINDS[0][0] and i % 2 == 0,
                    "consultation_fee_min": fmin, "consultation_fee_max": fmax,
                    "is_sample": True, "is_active": True,
                },
            )
            h_new += created

        m_new = 0
        for name, cat, pet, form, used, pmin, pmax, rx, notes in MEDICATIONS:
            _, created = Medication.objects.update_or_create(
                name=name, pet_type=pet,
                defaults={"category": cat, "form": form, "used_for": used, "price_min": pmin,
                          "price_max": pmax, "prescription_required": rx, "notes": notes, "is_active": True},
            )
            m_new += created

        self.stdout.write(self.style.SUCCESS(
            f"Hospitals: {Hospital.objects.count()} (new {h_new}). "
            f"Medications: {Medication.objects.count()} (new {m_new})."))