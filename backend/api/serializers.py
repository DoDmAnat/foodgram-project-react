from django.core.validators import MinValueValidator
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")
    id = serializers.ReadOnlyField(source="ingredient.id")
    amount = serializers.IntegerField(validators=[MinValueValidator(1)], required=True)

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    text = serializers.CharField(trim_whitespace=False)
    cooking_time = serializers.IntegerField(validators=[MinValueValidator(1)])
    ingredients = serializers.SerializerMethodField(read_only=True)

    def get_ingredients(self, obj):
        ingredients = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=request.user).exists()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
        error_messages={'does_not_exist': 'Указанного тега не существует'}
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()
    def validate_tags(self, tags):
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError("Такого тега не существует")
        return tags

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                "Время приготовления не может быть меньше одной минуты"
            )
        return cooking_time

    def validate_ingredients(self, ingredients):
        ingredients_list = []
        if not ingredients:
            raise serializers.ValidationError("Ингредиенты отсутствуют")
        for ingredient in ingredients:
            ingredient_id = ingredient.get("id")
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError("Ингредиенты не могут повторяться")
            ingredients_list.append(ingredient_id)
            if int(ingredient.get("amount")) < 1:
                raise serializers.ValidationError(
                    "Количество ингредиента должно быть не менее одного"
                )
        return ingredients

    def __create_ingredients(self, recipe, ingredients):
        ingredient_list = [] 
        for ingredient_data in ingredients: 
            ingredient_list.append( 
                IngredientAmount( 
                    ingredient=ingredient_data.pop("id"), 
                    amount=ingredient_data.pop("amount"), 
                    recipe=recipe, 
                ) 
            ) 
        IngredientAmount.objects.bulk_create(ingredient_list)

    @transaction.atomic
    def create(self, validated_data):
        if not validated_data.get("tags"):
            raise KeyError("Отсутствует тэг")
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.__create_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if "tags" in validated_data:
            instance.tags.set(validated_data.pop("tags"))
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            instance.ingredients.clear()
            self.__create_ingredients(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipesSerializer(
            instance, context={"request": self.context.get("request")}
        ).data

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )


class FavoriteSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = data["user"]
        if user.favorites.filter(recipe=data["recipe"]).exists():
            raise serializers.ValidationError("Рецепт уже в избранном.")
        return data

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class CartSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = data["user"]
        if user.shopping_cart.filter(recipe=data["recipe"]).exists():
            raise serializers.ValidationError("Рецепт уже в корзине")
        return data

    def to_representation(self, instance):
        return FavoriteSerializer(
            instance.recipe, context={"request": self.context.get("request")}
        ).data

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")
