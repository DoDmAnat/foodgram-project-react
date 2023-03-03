from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = "api"

v1_router = DefaultRouter()

v1_router.register("users", CustomUserViewSet, basename="users")
v1_router.register("ingredients", IngredientViewSet, basename="ingredients")
v1_router.register("tags", TagViewSet, basename="tags")
v1_router.register("recipes", RecipeViewSet, basename="recipes")

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]