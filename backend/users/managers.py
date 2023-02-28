from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self, email, password, username, first_name, last_name, **extra_fields
    ):
        if not email:
            raise ValueError("Укажите Email")
        if not username:
            raise ValueError("Укажите логин")
        if not (first_name or last_name):
            raise ValueError("Необходимо указать имя и фамилию")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email, password, username, first_name, last_name, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

    def create_superuser(
        self, email, password, username, first_name, last_name, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
