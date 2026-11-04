from django.contrib import admin

from .models import Booking, BookingItem, Invoice, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "pet_type", "size", "unit", "price", "is_active")
    list_filter = ("category", "pet_type", "is_active")
    list_editable = ("price", "is_active")


admin.site.register([Booking, BookingItem, Invoice])