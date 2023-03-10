from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = "api"

router = DefaultRouter()

router.register("users", CustomUserViewSet, basename="users")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("tags", TagViewSet, basename="tags")
router.register("recipes", RecipeViewSet, basename="recipes")

main_urls = [
    path("", include("djoser.urls")),
    path("", include(router.urls)),

]
urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(main_urls)),
]
