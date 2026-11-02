"""Money and invoice logic, kept separate from views and serializers so it is easy to test."""
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.db import transaction
from django.utils import timezone

TWO_PLACES = Decimal("0.01")


def money(value):
    return Decimal(value).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def get_gst_rate():
    """GST percentage. Set PET_SERVICE_GST_RATE in settings.py to change it (default 18)."""
    return Decimal(str(getattr(settings, "PET_SERVICE_GST_RATE", "18")))


def line_total(unit_price, quantity):
    return money(Decimal(unit_price) * Decimal(quantity))


def calculate_totals(line_totals, gst_rate):
    subtotal = money(sum(line_totals, Decimal("0")))
    gst_amount = money(subtotal * Decimal(gst_rate) / Decimal("100"))
    return subtotal, gst_amount, money(subtotal + gst_amount)


def invoice_number(booking_id, when=None):
    when = when or timezone.now()
    return f"PF-{when:%Y}-{booking_id:05d}"


@transaction.atomic
def create_booking(user, customer, items):
    """
    customer: dict of Booking fields (customer_name, customer_phone, pet_name, notes, service_date)
    items:    list of (PetService, quantity)
    Returns the new Booking with its items and invoice.
    """
    from .models import Booking, BookingItem, Invoice

    booking = Booking.objects.create(user=user, **customer)

    rows, totals = [], []
    for service, quantity in items:
        total = line_total(service.price, quantity)
        label = service.name if service.size == "Any" else f"{service.name} ({service.size})"
        rows.append(
            BookingItem(
                booking=booking,
                service=service,
                service_name=label,
                unit=service.unit,
                unit_price=service.price,
                quantity=quantity,
                line_total=total,
            )
        )
        totals.append(total)
    BookingItem.objects.bulk_create(rows)

    rate = get_gst_rate()
    subtotal, gst_amount, total = calculate_totals(totals, rate)
    Invoice.objects.create(
        booking=booking,
        number=invoice_number(booking.pk),
        subtotal=subtotal,
        gst_rate=rate,
        gst_amount=gst_amount,
        total=total,
    )
    return booking