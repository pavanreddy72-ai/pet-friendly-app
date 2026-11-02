from rest_framework import serializers

from .models import AdoptionListing, SaleListing

# Statuses an owner may set on their own listing
OWNER_STATUSES = {"active", "reserved", "completed"}
MAX_PHOTO_MB = 5

BASE_FIELDS = (
    "id",
    "owner",
    "owner_email",
    "is_owner",
    "pet_name",
    "species",
    "breed",
    "age_description",
    "gender",
    "vaccinated",
    "neutered",
    "description",
    "location",
    "contact_phone",
    "photo",
    "image_url",
    "display_image",
    "status",
    "created_at",
    "updated_at",
)
READ_ONLY = ("id", "owner", "owner_email", "is_owner", "display_image", "created_at", "updated_at")


class BaseListingSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)
    is_owner = serializers.SerializerMethodField()
    display_image = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return bool(
            request and request.user.is_authenticated and request.user.id == obj.owner_id
        )

    def get_display_image(self, obj):
        if obj.photo:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return obj.image_url

    def validate_photo(self, value):
        if value and value.size > MAX_PHOTO_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Photo must be under {MAX_PHOTO_MB} MB.")
        return value

    def validate_status(self, value):
        request = self.context.get("request")
        if request and request.user.is_staff:
            return value
        if value not in OWNER_STATUSES:
            raise serializers.ValidationError("You can only set Active, Reserved or Completed.")
        if self.instance and self.instance.status not in OWNER_STATUSES:
            raise serializers.ValidationError(
                "This listing is not approved, so its status cannot be changed."
            )
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        # Contact details are only shown to logged-in users
        if not (request and request.user.is_authenticated):
            data.pop("contact_phone", None)
            data.pop("owner_email", None)
        return data


class AdoptionListingSerializer(BaseListingSerializer):
    class Meta:
        model = AdoptionListing
        fields = BASE_FIELDS + ("adoption_fee",)
        read_only_fields = READ_ONLY


class SaleListingSerializer(BaseListingSerializer):
    class Meta:
        model = SaleListing
        fields = BASE_FIELDS + ("price",)
        read_only_fields = READ_ONLY