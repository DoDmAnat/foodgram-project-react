from django.contrib import admin
from .models import Tag, Ingredient, Recipe

admin.site.register(Tag)
admin.site.register(Ingredient)


@admin.register(Recipe)
class ResipesAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "time")
    filter_horizontal = [
        "ingredients",
        "tag",
    ]
