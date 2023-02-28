from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    ADMIN = "admin"
    USER = "user"
    ROLES = (
        (ADMIN, "Administrator"),
        (USER, "User"),
    )
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField("Email", max_length=254, unique=True)
    role = models.CharField(
        "Роль пользователя", choices=ROLES, max_length=50, default=USER
    )

    objects = UserManager()
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "password", ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["author", "user"],
                                    name="unique_follow")
        ]
        ordering = ("author", "user")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
