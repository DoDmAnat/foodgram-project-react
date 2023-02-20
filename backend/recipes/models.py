from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model

class Recipe(models.Model):
    author = models.ForeignKey
    name = models.CharField(max_length=100)
    picture = models.ImageField()
    description = models.CharField()
    ingredients = models.ManyToManyField
    tag = models.ManyToManyField
    time = models.DateTimeField


class Tag(models.Model):
    name = models.CharField
    hex = models.CharField
    slug = models.SlugField


class Ingredient(models.Model):
    name = models.CharField
    quantity = models.IntegerField
    units = models.CharField