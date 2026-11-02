from django.apps import AppConfig


class PetServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pet_service"
    verbose_name = "Pet services"