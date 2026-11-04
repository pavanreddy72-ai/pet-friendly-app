
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand, CommandError

from products.models import Product


API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "PetFriendlyPortfolio/1.0 (educational project)"

IGNORED_WORDS = {
    "the", "and", "for", "with", "small", "large", "pack",
    "pet", "pets", "product", "image", "photo", "file",
}


def request_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    last_error = None

    for attempt in range(4):
        request = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in (429, 500, 502, 503, 504):
                time.sleep(2 * (attempt + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(attempt + 1)

    raise RuntimeError(f"Wikimedia request failed: {last_error}")


def clean_name(name):
    return re.sub(
        r"\s*-\s*(Small|Large)\s+Pack$",
        "",
        name.strip(),
        flags=re.IGNORECASE,
    )


def words(value):
    return {
        word for word in re.findall(r"[a-z0-9]+", value.lower())
        if len(word) > 2 and word not in IGNORED_WORDS
    }


def image_score(product_name, file_title):
    product_words = words(product_name)
    title_words = words(file_title.replace("File:", ""))
    if not product_words:
        return 0
    return len(product_words & title_words)


def search_commons(product_name, pet_type, used_titles):
    animal = (pet_type or "").strip().lower()
    queries = [
        f'"{product_name}" {animal}',
        f"{product_name} {animal}",
        product_name,
    ]

    candidates = {}

    for query in dict.fromkeys(queries):
        params = {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 15,
            "prop": "imageinfo",
            "iiprop": "url|mime",
            "iiurlwidth": 700,
        }

        data = request_json(params)
        pages = data.get("query", {}).get("pages", [])

        for page in pages:
            title = page.get("title", "")
            info_list = page.get("imageinfo", [])

            if not info_list or title in used_titles:
                continue

            info = info_list[0]
            mime = info.get("mime", "")

            if mime not in ("image/jpeg", "image/png", "image/webp"):
                continue

            image_url = info.get("thumburl") or info.get("url", "")
            if not image_url.startswith("https://"):
                continue

            score = image_score(product_name, title)

            if score:
                candidates[title] = {
                    "title": title,
                    "url": image_url,
                    "score": score,
                    "source": info.get("descriptionurl", ""),
                }

        time.sleep(0.5)

    if not candidates:
        return None

    ranked = sorted(
        candidates.values(),
        key=lambda item: (item["score"], item["title"]),
        reverse=True,
    )

    return ranked[0]


class Command(BaseCommand):
    help = "Find product-specific photographs from Wikimedia Commons."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=5)
        parser.add_argument("--all", action="store_true")
        parser.add_argument("--refresh-images", action="store_true")
        parser.add_argument("--category", type=str, default="")

    def handle(self, *args, **options):
        if options["limit"] < 1:
            raise CommandError("--limit must be at least 1")

        queryset = Product.objects.filter(is_active=True).order_by("id")

        if options["category"]:
            queryset = queryset.filter(
                category__iexact=options["category"].strip()
            )

        groups = {}

        for product in queryset:
            base_name = clean_name(product.name)
            key = (base_name.lower(), (product.pet_type or "").lower())

            groups.setdefault(key, {
                "name": base_name,
                "pet_type": product.pet_type,
                "products": [],
            })["products"].append(product)

        work = []

        for group in groups.values():
            variants = group["products"]

            if not options["refresh_images"]:
                if all(product.image_url for product in variants):
                    continue

            work.append(group)

        if not options["all"]:
            work = work[:options["limit"]]

        self.stdout.write(f"Active products: {queryset.count()}")
        self.stdout.write(f"Groups selected: {len(work)}")

        used_titles = set()
        found = 0
        missing = 0
        errors = 0

        for index, group in enumerate(work, 1):
            name = group["name"]
            self.stdout.write(
                f"\n[{index}/{len(work)}] {name}"
            )

            try:
                result = search_commons(
                    name,
                    group["pet_type"],
                    used_titles,
                )

                if not result:
                    missing += 1
                    self.stdout.write(
                        self.style.WARNING("No suitable image found.")
                    )
                    continue

                for product in group["products"]:
                    product.image_url = result["url"]
                    product.save(update_fields=["image_url"])

                used_titles.add(result["title"])
                found += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Image: {result['title']}"
                    )
                )
                self.stdout.write(result["url"])

                time.sleep(1)

            except Exception as exc:
                errors += 1
                self.stderr.write(
                    self.style.ERROR(f"Failed: {exc}")
                )

        self.stdout.write("\n--- SUMMARY ---")
        self.stdout.write(f"Images found: {found}")
        self.stdout.write(f"Not found: {missing}")
        self.stdout.write(f"Errors: {errors}")
        self.stdout.write(
            f"Products with image URLs: "
            f"{Product.objects.filter(is_active=True).exclude(image_url='').count()}"
        )
        self.stdout.write(
            f"Active products: "
            f"{Product.objects.filter(is_active=True).count()}"
        )
