from django.contrib import admin

from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "email",
        "username",
    )
    search_fields = (
        "email",
        "username",
    )


@admin.register(Follow)
class FollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    list_filter = ("user", "author")
    search_fields = ("user", "author")
