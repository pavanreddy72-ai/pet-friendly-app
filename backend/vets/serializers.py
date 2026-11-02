from rest_framework import serializers

from .models import Hospital, Medication


class HospitalSerializer(serializers.ModelSerializer):
    services_list = serializers.SerializerMethodField()
    fee_label = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = ("id", "name", "area", "city", "address", "phone", "services", "services_list",
                  "pet_types", "open_hours", "emergency_24x7", "home_visits",
                  "consultation_fee_min", "consultation_fee_max", "fee_label", "is_sample")

    def get_services_list(self, obj):
        return [s.strip() for s in obj.services.split(",") if s.strip()]

    def get_fee_label(self, obj):
        if not obj.consultation_fee_max:
            return ""
        return f"\u20b9{obj.consultation_fee_min}\u2013{obj.consultation_fee_max} consultation"


class MedicationSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    price_label = serializers.SerializerMethodField()

    class Meta:
        model = Medication
        fields = ("id", "name", "category", "category_label", "pet_type", "form", "used_for",
                  "price_min", "price_max", "price_label", "prescription_required", "notes")

    def get_price_label(self, obj):
        if not obj.price_max:
            return ""
        return f"\u20b9{obj.price_min}\u2013{obj.price_max}"