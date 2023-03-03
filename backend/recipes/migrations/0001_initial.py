# Generated by Django 4.1.7 on 2023-02-28 11:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Корзина",
                "verbose_name_plural": "Корзины",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранные",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Название ингредиента"
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(max_length=20, verbose_name="Единица измерения"),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="IngredientAmount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1,
                                message="Минимальное количество ингредиента - 1",
                            )
                        ],
                        verbose_name="Количество",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент в рецепте",
                "verbose_name_plural": "Ингредиенты в рецепте",
                "ordering": ("recipe", "ingredient"),
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Название рецепта"),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="recipes/", verbose_name="Картинка рецепта"
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание рецепта")),
                (
                    "time",
                    models.PositiveSmallIntegerField(
                        verbose_name="Время приготовления"
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
                "ordering": ("-pub_date",),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
                ("slug", models.SlugField(max_length=10, unique=True)),
                (
                    "color",
                    models.CharField(
                        default="#ffffff", max_length=7, verbose_name="HEX-код"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ("-id",),
            },
        ),
        migrations.AddConstraint(
            model_name="tag",
            constraint=models.UniqueConstraint(fields=("slug",), name="unique_slug"),
        ),
        migrations.AddField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор рецепта",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="ingredients",
                through="recipes.IngredientAmount",
                to="recipes.ingredient",
                verbose_name="Ингредиенты",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="recipe", to="recipes.tag", verbose_name="Тэг"
            ),
        ),
        migrations.AddField(
            model_name="ingredientamount",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_amount",
                to="recipes.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AddField(
            model_name="ingredientamount",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_amount",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("measurement_unit", "name"),
                name="Уже существует такой ингредиент",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorites",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddConstraint(
            model_name="ingredientamount",
            constraint=models.UniqueConstraint(
                fields=("ingredient", "recipe"), name="Такой ингредиент уже добавлен"
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="Рецепт уже в избранном"
            ),
        ),
        migrations.AddConstraint(
            model_name="cart",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="Рецепт уже в корзине"
            ),
        ),
    ]