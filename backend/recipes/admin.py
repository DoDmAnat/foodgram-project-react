from django.contrib import admin
from .models import Tag, Ingredient, Recipe


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "units",
    )
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "name",
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
