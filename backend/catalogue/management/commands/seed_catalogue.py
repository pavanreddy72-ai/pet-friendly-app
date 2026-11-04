import json
import time
import urllib.error
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand
from django.db.models import ProtectedError

from catalogue.models import Breed, PetCategory
from catalogue.seed_data import (
    CATEGORIES,
    REMOVE,
    SINGULAR,
    build_profile,
    iter_rows,
)

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = (
    "PetFriendlyCatalogue/2.0 "
    "(https://github.com/pavanreddy72-ai; educational portfolio project)"
)


def _get_json(url):
    """GET with retries; waits and retries on rate limits (429/503)."""
    last_error = None
    for attempt in range(4):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in (429, 503):
                time.sleep(3 * (attempt + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"Request failed after retries: {last_error}")


def _search_image(query):
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 0,
        "gsrlimit": 3,
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": 600,
        "pilimit": 3,
    })
    data = _get_json(f"{API}?{params}")
    pages = data.get("query", {}).get("pages", {})
    for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        source = (page.get("thumbnail") or {}).get("source")
        if source:
            return source, page.get("title", "")
    return None


def find_animal_image(name, category):
    """Return (url, title) or None if no image exists.
    Raises an exception only on network problems."""
    singular = SINGULAR.get(category, "")
    for query in (f"{name} {singular}", name, f"{name} ({singular})"):
        result = _search_image(query)
        if result:
            return result
        time.sleep(0.2)
    return None


class Command(BaseCommand):
    help = "Seed pet categories and 400+ catalogue entries with images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh-images",
            action="store_true",
            help="Re-fetch images even if an image_url already exists",
        )
        parser.add_argument(
            "--no-images",
            action="store_true",
            help="Skip image lookups (fast; images can be added later)",
        )

    def handle(self, *args, **options):
        refresh = options["refresh_images"]
        no_images = options["no_images"]

        removed = 0
        for rm_cat, rm_name in REMOVE:
            for old_breed in Breed.objects.filter(category__name=rm_cat, name__iexact=rm_name):
                try:
                    old_breed.delete()
                    removed += 1
                except ProtectedError:
                    self.stderr.write(f"Could not remove {rm_cat} | {rm_name} (in use)")
        self.stdout.write(f"Removed duplicate entries: {removed}")

        categories_created = breeds_created = breeds_updated = 0
        images_found = images_not_on_wikipedia = image_errors = 0
        consecutive_errors = 0

        for cat_name, slug, emoji in CATEGORIES:
            category, created = PetCategory.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": cat_name,
                    "emoji": emoji,
                    "description": (
                        f"Explore {cat_name.lower()}, their characteristics, "
                        "care requirements and suitability."
                    ),
                    "is_active": True,
                },
            )
            if created:
                categories_created += 1

            self.stdout.write(self.style.NOTICE(f"Seeding category: {cat_name}"))

            for name, height, weight, life, tags in iter_rows(cat_name):
                existing = Breed.objects.filter(category=category, name__iexact=name).first()
                profile = build_profile(name, cat_name, height, weight, life, tags)
                old_image = existing.image_url if existing else ""

                if old_image and not refresh:
                    profile["image_url"] = old_image
                elif no_images:
                    profile["image_url"] = old_image
                else:
                    try:
                        result = find_animal_image(name, cat_name)
                        consecutive_errors = 0
                        if result:
                            profile["image_url"] = result[0]
                            images_found += 1
                        else:
                            profile["image_url"] = old_image
                            images_not_on_wikipedia += 1
                    except Exception as exc:
                        image_errors += 1
                        consecutive_errors += 1
                        profile["image_url"] = old_image
                        if image_errors <= 5:
                            self.stderr.write(f"Image lookup failed for {name}: {exc}")
                        if consecutive_errors >= 8:
                            self.stderr.write(self.style.ERROR(
                                "8 network errors in a row - stopping image lookups. "
                                "Check your internet, wait a few minutes, then run: "
                                "python manage.py seed_catalogue"
                            ))
                            no_images = True
                    time.sleep(0.5)

                if existing:
                    for field, value in profile.items():
                        setattr(existing, field, value)
                    existing.name = name
                    existing.save()
                    breeds_updated += 1
                else:
                    Breed.objects.create(category=category, name=name, **profile)
                    breeds_created += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Catalogue seeding completed."))
        self.stdout.write(f"Categories created: {categories_created}")
        self.stdout.write(f"Breeds created: {breeds_created}")
        self.stdout.write(f"Breeds updated: {breeds_updated}")
        self.stdout.write(f"Images found: {images_found}")
        self.stdout.write(f"No image on Wikipedia: {images_not_on_wikipedia}")
        self.stdout.write(f"Network errors: {image_errors}")
        self.stdout.write(
            f"Entries with an image: {Breed.objects.exclude(image_url='').count()}"
        )
        self.stdout.write(
            f"Total active catalogue entries: {Breed.objects.filter(is_active=True).count()}"
        )