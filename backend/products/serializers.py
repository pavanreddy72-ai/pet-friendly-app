from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "category", "category_label", "pet_type", "pack",
                  "price", "description", "image_url", "in_stock")