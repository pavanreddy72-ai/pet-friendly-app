from django.contrib import admin
from django.utils import timezone

from .models import Booking, BookingItem, Invoice, PetService


@admin.register(PetService)
class PetServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "pet_type", "size", "unit", "price", "is_active")
    list_filter = ("category", "pet_type", "size", "unit", "is_active")
    search_fields = ("name",)
    list_editable = ("price", "is_active")


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0
    readonly_fields = ("service", "service_name", "unit", "unit_price", "quantity", "line_total")
    can_delete = False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "pet_name", "service_date", "status", "created_at")
    list_filter = ("status", "service_date")
    search_fields = ("customer_name", "pet_name", "customer_phone")
    inlines = [BookingItemInline]


@admin.action(description="Mark selected invoices as paid")
def mark_paid(modeladmin, request, queryset):
    queryset.filter(is_paid=False).update(is_paid=True, paid_at=timezone.now())


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "booking", "subtotal", "gst_amount", "total", "is_paid", "issued_at")
    list_filter = ("is_paid",)
    search_fields = ("number", "booking__customer_name")
    readonly_fields = ("booking", "number", "subtotal", "gst_rate", "gst_amount", "total", "issued_at")
    actions = [mark_paid]