from django.contrib import admin

from .models import AdoptionListing, SaleListing


@admin.action(description="Mark selected as Active")
def make_active(modeladmin, request, queryset):
    queryset.update(status="active")


@admin.action(description="Reject selected")
def reject(modeladmin, request, queryset):
    queryset.update(status="rejected")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("pet_name", "species", "location", "status", "owner", "created_at")
    list_filter = ("status", "species", "gender")
    search_fields = ("pet_name", "breed", "location")
    actions = [make_active, reject]


admin.site.register(AdoptionListing, ListingAdmin)
admin.site.register(SaleListing, ListingAdmin)