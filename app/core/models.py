from __future__ import annotations
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    def create(self, first_name, last_name, username, email, password) -> User:
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name, last_name, username, email, password
    ) -> User:
        user = self.create(first_name, last_name, username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

    def normalize_email(self, email: str):
        return email.lower()


class User(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    first_surname = models.CharField(max_length=50)
    second_surname = models.CharField(max_length=50)
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator],
    )
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "username", "email"]

    def __str__(self) -> str:
        return self.username


class Subject(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    code = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=255, unique=True)
    credits = models.IntegerField(default=0, validators=[MinValueValidator("0")])
    is_lab = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
