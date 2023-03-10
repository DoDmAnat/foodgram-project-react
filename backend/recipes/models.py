from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w]+\Z",
                message="Допускаются только буквы и цифры",
            )
        ],
    )
    slug = models.SlugField(max_length=10, unique=True)
    color = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name="HEX-код",
        validators=[
            RegexValidator(
                regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
                message="Неправильный формат HEX Color",
            )
        ],
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        constraints = [
            models.UniqueConstraint(
                fields=["slug"],
                name="Такой тэг уже добавлен",
            )
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Название ингредиента")
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name="Единица измерения")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["measurement_unit", "name"],
                name="Уже существует такой ингредиент",
            )
        ]

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="ingredient_amount",
        to="Recipe",
        verbose_name="Рецепт",
        db_index=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_amount",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                limit_value=1, message="Минимальное количество ингредиента - 1"
            ),
        ),
        verbose_name="Количество",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="Такой ингредиент уже добавлен",
            )
        ]
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        ordering = ("recipe", "ingredient")

    def __str__(self):
        return f"{self.ingredient}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(max_length=200, verbose_name="Название рецепта")
    image = models.ImageField(upload_to="recipes/",
                              verbose_name="Картинка рецепта")
    text = models.TextField(verbose_name="Описание рецепта")
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipes",
        through="IngredientAmount",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(Tag, related_name="recipes",
                                  verbose_name="Тэг")
    cooking_time = models.PositiveSmallIntegerField("Время приготовления")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


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
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="Рецепт уже в избранном",
            )
        ]

    def __str__(self):
        return f"Избранное пользователя {self.user}: {self.recipe}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="shopping_cart",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="Рецепт уже в корзине",
            )
        ]
        ordering = ("-id",)
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user}: {self.recipe}"
