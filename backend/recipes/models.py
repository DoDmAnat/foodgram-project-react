from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=7, unique=True, verbose_name="HEX-код")
    slug = models.SlugField(max_length=10, unique=True)

    class Meta:
        ordering = ("slug",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        constraints = [models.UniqueConstraint(fields=["slug"], name="unique_slug")]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ингредиента")
    units = models.CharField(max_length=20, verbose_name="Единица измерения")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(max_length=200, verbose_name="Название рецепта")
    image = models.ImageField(upload_to="resipes/", verbose_name="Картинка рецепта")
    description = models.TextField(verbose_name="Описание рецепта")
    ingredients = models.ManyToManyField(Ingredient)
    tag = models.ManyToManyField(Tag)
    time = models.PositiveSmallIntegerField("Время приготовления")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name
