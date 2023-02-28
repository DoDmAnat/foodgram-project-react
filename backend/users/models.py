from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField("Логин", max_length=100, null=True, blank=True)
    email = models.EmailField(
        unique=True,
        max_length=254,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
