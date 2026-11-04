from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Booking, BookingItem, Invoice, Service

# Demo GST rate. Confirm the correct rate for your business before real use.
GST_RATE = Decimal("18")


def money(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class ServiceSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    unit_label = serializers.CharField(source="get_unit_display", read_only=True)
    price_label = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ("id", "category", "category_label", "name", "pet_type", "size",
                  "unit", "unit_label", "price", "price_label", "description")

    def get_price_label(self, obj):
        amount = f"{obj.price:.0f}" if obj.price == obj.price.to_integral() else f"{obj.price:.2f}"
        return f"\u20b9{amount} {obj.get_unit_display()}"


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = ("id", "service", "service_name", "unit", "unit_price", "quantity", "line_total")


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ("number", "subtotal", "gst_rate", "gst_amount", "total", "issued_at")


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "customer_name", "customer_phone", "pet_name", "notes",
                  "status", "created_at", "items", "invoice")


class BookingItemInputSerializer(serializers.Serializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.filter(is_active=True))
    quantity = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=Decimal("0.5"))


class BookingCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=150)
    customer_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    pet_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    items = BookingItemInputSerializer(many=True, allow_empty=False)

    def create(self, validated_data):
        items = validated_data.pop("items")
        user = self.context["request"].user

        with transaction.atomic():
            booking = Booking.objects.create(user=user, **validated_data)
            subtotal = Decimal("0")

            for item in items:
                service, quantity = item["service"], item["quantity"]
                line_total = money(service.price * quantity)
                label = service.name if service.size == "Any" else f"{service.name} ({service.size})"
                BookingItem.objects.create(
                    booking=booking, service=service, service_name=label, unit=service.unit,
                    unit_price=service.price, quantity=quantity, line_total=line_total,
                )
                subtotal += line_total

            subtotal = money(subtotal)
            gst_amount = money(subtotal * GST_RATE / 100)
            Invoice.objects.create(
                booking=booking,
                number=f"PF-{timezone.now():%Y}-{booking.pk:05d}",
                subtotal=subtotal, gst_rate=GST_RATE, gst_amount=gst_amount,
                total=subtotal + gst_amount,
            )
        return booking