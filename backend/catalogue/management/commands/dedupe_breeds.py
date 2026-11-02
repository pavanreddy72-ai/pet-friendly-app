from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import ProtectedError

from catalogue.models import Breed


class Command(BaseCommand):
    help = (
        "Find duplicate breeds (same category, same name ignoring case/spaces). "
        "Dry run by default; pass --apply to delete the extras."
    )

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Actually delete duplicates")

    def handle(self, *args, **options):
        groups = defaultdict(list)
        for breed in Breed.objects.select_related("category").all():
            key = (breed.category_id, " ".join(breed.name.lower().split()))
            groups[key].append(breed)

        duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}
        if not duplicate_groups:
            self.stdout.write(self.style.SUCCESS("No duplicates found."))
            return

        removed = skipped = 0
        for items in duplicate_groups.values():
            # Keep the entry with an image, then the longest description, then the oldest id
            items.sort(key=lambda b: (not b.image_url, -len(b.description or ""), b.id))
            keep, extras = items[0], items[1:]
            self.stdout.write(
                f"{keep.category.name}: keeping '{keep.name}' (id {keep.id}); "
                f"extras: {[b.id for b in extras]}"
            )
            if not options["apply"]:
                continue
            for extra in extras:
                try:
                    extra.delete()
                    removed += 1
                except ProtectedError:
                    skipped += 1
                    self.stderr.write(f"  Could not delete id {extra.id}: it is referenced elsewhere")

        if options["apply"]:
            self.stdout.write(self.style.SUCCESS(f"Removed {removed} duplicates, skipped {skipped}."))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"{len(duplicate_groups)} duplicate group(s). Dry run only - re-run with --apply."
                )
            )