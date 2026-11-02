from django.contrib import admin

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "area", "city", "price_min", "price_max", "pet_fee", "is_sample")
    list_filter = ("category", "city", "is_sample")
    search_fields = ("name", "area")