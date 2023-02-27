from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    list_filter = ("user",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    list_filter = ("user",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "amount",
        "units",
        "ingredient_name",
    )
    list_filter = ("recipe",)

    def ingredient_name(self, obj):
        return obj.ingredient.name

    def units(self, obj):
        return obj.ingredient.measurement_unit

    units.short_description = "Единица измерения"
    ingredient_name.short_description = "Ингредиент"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInline,)
    list_display = (
        "pk",
        "author",
        "name",
    )
    list_filter = ("name", "author", "tags")
    search_fields = ("name", "author", "tags")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)
