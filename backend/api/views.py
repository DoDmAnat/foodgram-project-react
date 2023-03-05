from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipesSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (IngredientFilter,)
    search_fields = ("^name",)
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSerializer
        return RecipeCreateSerializer

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {"errors": "Рецепт уже добавлен."}, status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Нет такого рецепта или он уже был удален!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=("post", "delete"), detail=True, permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = request.user

        if request.method == "POST":
            return self.add_to(ShoppingCart, user, pk)

        if request.method == "DELETE":
            return self.delete_from(ShoppingCart, user, pk)

    @action(
        methods=("post", "delete"), detail=True, permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = request.user
        if request.method == "POST":
            return self.add_to(Favorite, user, pk)
        elif request.method == "DELETE":
            return self.delete_from(Favorite, user, pk)

    @action(
        methods=("get",),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipes_query = Recipe.objects.filter(
            shoppingcart_recipes__owner=self.request.user
        ).all()

        ingredients_query = (
            recipes_query.values(
                "ingredients_recipes__ingredient__name",
                "ingredients_recipes__ingredient__measurement_unit",
            )
            .annotate(amount=Sum("ingredients_recipes__amount"))
            .order_by()
        )

        text = "\n".join(
            [
                f"{item['ingredients_recipes__ingredient__name']}: "
                f"{item['amount']}, "
                f"{item['ingredients_recipes__ingredient__measurement_unit']}"
                for item in ingredients_query
            ]
        )
        filename = "shopping_card.txt"
        response = HttpResponse(text, content_type="text/plain")
        response["Content-Disposition"] = f"attachment'; filename={filename}"

        return response