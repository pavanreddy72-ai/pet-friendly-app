from django.urls import path

from .views import BreedListView, PetCategoryListView

urlpatterns = [
    path("", BreedListView.as_view(), name="breed-list-root"),
    path("breeds/", BreedListView.as_view(), name="breed-list"),
    path("categories/", PetCategoryListView.as_view(), name="category-list"),
]