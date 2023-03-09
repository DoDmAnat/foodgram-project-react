from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (ShoppingCart, Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipesSerializer, TagSerializer)


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


# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     # serializer_class = RecipeCreateSerializer
#     pagination_class = CustomPagination
#     permission_classes = (IsAuthorOrReadOnly,)
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = RecipeFilter
    

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return RecipesSerializer
#         return RecipeCreateSerializer

#     def __add_to(self, model, user, pk):
#         recipe = get_object_or_404(Recipe, id=pk)
#         model.objects.create(user=user, recipe=recipe)
#         serializer = FavoriteSerializer(recipe)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def __delete_from(self, model, user, pk):
#         obj = model.objects.filter(user=user, recipe__id=pk)
#         if obj.exists():
#             obj.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(
#             {"errors": "Нет такого рецепта или он уже был удален!"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     @action(
#         methods=("post", "delete"), detail=True, permission_classes=(IsAuthenticated,)
#     )
#     def shopping_cart(self, request, pk):
#         user = request.user

#         if request.method == "POST":
#             return self.__add_to(ShoppingCart, user, pk)

#         if request.method == "DELETE":
#             return self.__delete_from(ShoppingCart, user, pk)

#     @action(
#         methods=("post", "delete"), detail=True, permission_classes=(IsAuthenticated,)
#     )
#     def favorite(self, request, pk):
#         user = request.user
#         if request.method == "POST":
#             return self.__add_to(Favorite, user, pk)
#         elif request.method == "DELETE":
#             return self.__delete_from(Favorite, user, pk)

#     @action(methods=("get"), detail=False, permission_classes=(IsAuthenticated,))
#     def download_shopping_cart(self, request): 
#         user = request.user
#         if not user.shopping_cart.exists():
#             return Response(status=HTTP_400_BAD_REQUEST)
#         ingredients = IngredientAmount.objects.filter(
#             recipe__shopping_cart__user=user
#         ).values(
#             'ingredient__name',
#             'ingredient__measurement_unit'
#         ).annotate(amount=Sum('amount'))
#         today = datetime.today()
#         shopping_list = (
#             f'Список покупок пользователя: {user}\n'
#             f'Дата: {today:%Y-%m-%d}\n'
#         )
#         shopping_list += '\n'.join([
#             f'- {ingredient["ingredient__name"]} - {ingredient["amount"]} '
#             f'{ingredient["ingredient__measurement_unit"]}'
#             for ingredient in ingredients
#         ])
#         filename = f'{user}_shopping_list.txt'
#         response = HttpResponse(shopping_list, content_type='text/plain')
#         response['Content-Disposition'] = f'attachment; filename={filename}'
#         return response
class RecipeViewSet(viewsets.ModelViewSet):
    """View представления рецептов"""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesSerializer
        return RecipeCreateSerializer
    
    def _post_method_actions(self, request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def _delete_method_actions(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_object = get_object_or_404(model, user=user, recipe=recipe)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self._post_method_actions(
            request=request, pk=pk, serializers=FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self._delete_method_actions(
            request=request, pk=pk, model=Favorite
        )
    
    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self._post_method_actions(
            request=request, pk=pk, serializers=CartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shoping_cart(self, request, pk):
        return self._delete_method_actions(
            request=request, pk=pk, model=ShoppingCart
        )
    
    @action(
        detail=False,
        methods=["GET"],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def download_basket(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('amount'))
        result = 'Cписок покупок:\n\nНазвание продукта - Кол-во/Ед.изм.\n'
        for ingredient in ingredients:
            result += ''.join([
                f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
                f'{ingredient["ingredient__measurement_unit"]} \n'
            ])
        filename = f'{user}_shopping_list.txt'
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
