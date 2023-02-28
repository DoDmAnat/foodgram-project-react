from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

app_name = "api"
router = DefaultRouter()

# router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register("tags", TagViewSet, basename="tags")
# router.register('recipes', RecipeViewSet, basename='recipes')
# router.register(
#     r'api/recipes/(?P<recipe_id>\d+)/favorite',
#     FavoriteViewSet,
#     basename='favorite',
# )

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
