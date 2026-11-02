from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "pet_type", "pack", "price", "in_stock", "is_active")
    list_filter = ("category", "pet_type", "in_stock", "is_active")
    search_fields = ("name",)
    list_editable = ("price", "in_stock", "is_active")