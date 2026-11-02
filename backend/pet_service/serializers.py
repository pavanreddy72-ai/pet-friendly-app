from decimal import Decimal

from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers

from . import billing
from .models import Booking, BookingItem, Invoice, PetService

MAX_ITEMS_PER_BOOKING = 30
phone_validator = RegexValidator(r"^[0-9+\-\s]{7,20}$", "Enter a valid phone number.")


class PetServiceSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    unit_label = serializers.CharField(source="get_unit_display", read_only=True)
    price_label = serializers.SerializerMethodField()

    class Meta:
        model = PetService
        fields = (
            "id", "category", "category_label", "name", "pet_type", "size",
            "unit", "unit_label", "price", "price_label", "description",
        )

    def get_price_label(self, obj):
        amount = obj.price
        text = f"{amount:,.0f}" if amount == amount.to_integral_value() else f"{amount:,.2f}"
        return f"\u20b9{text} {obj.get_unit_display()}"


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = ("id", "service", "service_name", "unit", "unit_price", "quantity", "line_total")


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            "number", "subtotal", "gst_rate", "gst_amount", "total",
            "is_paid", "paid_at", "issued_at",
        )


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id", "customer_name", "customer_phone", "pet_name", "service_date",
            "notes", "status", "created_at", "items", "invoice",
        )


class BookingItemInputSerializer(serializers.Serializer):
    service = serializers.PrimaryKeyRelatedField(queryset=PetService.objects.filter(is_active=True))
    quantity = serializers.DecimalField(
        max_digits=6, decimal_places=2, min_value=Decimal("0.5"), max_value=Decimal("365")
    )

    def validate(self, attrs):
        # Hours can be booked in half-hour steps; every other unit in whole numbers.
        step = Decimal("0.5") if attrs["service"].unit == "hour" else Decimal("1")
        if attrs["quantity"] % step != 0:
            unit = attrs["service"].get_unit_display().replace("per ", "")
            raise serializers.ValidationError(
                f"{attrs['service'].name}: quantity must be in steps of {step} {unit}."
            )
        return attrs


class BookingCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=150)
    customer_phone = serializers.CharField(
        max_length=20, required=False, allow_blank=True, validators=[phone_validator]
    )
    pet_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    service_date = serializers.DateField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    items = BookingItemInputSerializer(many=True, allow_empty=False)

    def validate_service_date(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError("Service date cannot be in the past.")
        return value

    def validate_items(self, items):
        if len(items) > MAX_ITEMS_PER_BOOKING:
            raise serializers.ValidationError(f"At most {MAX_ITEMS_PER_BOOKING} services per booking.")
        ids = [item["service"].pk for item in items]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError("Each service can be added only once. Change its quantity instead.")
        return items

    def create(self, validated_data):
        items = validated_data.pop("items")
        return billing.create_booking(
            user=self.context["request"].user,
            customer=validated_data,
            items=[(item["service"], item["quantity"]) for item in items],
        )