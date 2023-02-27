from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=10, unique=True)
    color = models.CharField(max_length=7, default="#ffffff", verbose_name="HEX-код")

    class Meta:
        ordering = ("slug",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        constraints = [models.UniqueConstraint(fields=["slug"], name="unique_slug")]

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color,
        )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название ингредиента")
    units = models.CharField(max_length=20, verbose_name="Единица измерения")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(
        max_length=200, related_name="author", verbose_name="Название рецепта"
    )
    image = models.ImageField(upload_to="images/", verbose_name="Картинка рецепта")
    description = models.TextField(verbose_name="Описание рецепта")
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="ingredients",
        on_delete=models.CASCADE,
        verbose_name="Ингредиенты",
    )
    tag = models.ManyToManyField(Tag, related_name="tag", verbose_name="Тэг")
    time = models.PositiveSmallIntegerField("Время приготовления")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


""" class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Рецепт",
        db_index=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name="Ингредиент",
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        ordering = ("recipe", "ingredient") """


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"], name="unique_favorite")
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )
