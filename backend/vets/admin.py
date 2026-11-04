from django.contrib import admin

from .models import Hospital, Medication


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "phone", "emergency_24x7", "home_visits", "is_sample", "is_active")
    list_filter = ("area", "emergency_24x7", "home_visits", "is_sample")
    search_fields = ("name", "area")


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "form", "pet_type", "is_active")
    list_filter = ("category", "form", "pet_type")
    search_fields = ("name", "used_for")