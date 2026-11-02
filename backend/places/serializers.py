from rest_framework import serializers

from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    amenities_list = serializers.SerializerMethodField()
    price_label = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ("id", "name", "category", "category_label", "area", "city", "location",
                  "address", "phone", "pet_policy", "amenities", "amenities_list",
                  "price_min", "price_max", "price_unit", "price_label", "pet_fee", "is_sample")

    def get_amenities_list(self, obj):
        return [a.strip() for a in obj.amenities.split(",") if a.strip()]

    def get_location(self, obj):
        return obj.area or obj.city

    def get_price_label(self, obj):
        if not obj.price_max:
            return "Free entry" if obj.price_unit == "entry" else ""
        return f"\u20b9{obj.price_min:,}\u2013{obj.price_max:,} {obj.get_price_unit_display()}"