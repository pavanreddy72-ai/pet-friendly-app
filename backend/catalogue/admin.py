from django.contrib import admin
from .models import Breed, PetCategory


@admin.register(PetCategory)
class PetCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("is_active",)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "size", "is_active")
    search_fields = ("name", "category__name")
    list_filter = ("category", "size", "is_active")