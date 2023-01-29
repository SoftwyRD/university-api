from __future__ import annotations
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
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
    id = models.AutoField(primary_key=True, unique=True, editable=False)
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
    credits = models.IntegerField(
        default=0, validators=[MinValueValidator("0")]
    )
    is_lab = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Weekday(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.name


class Selection(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class SelectionSection(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    selection_id = models.ForeignKey(Selection, on_delete=models.SET_NULL)
    section = models.IntegerField(
        default=1, validators=[MinValueValidator("0")]
    )
    subject_id = models.ForeignKey(Subject, on_delete=models.SET_NULL)
    professor = models.CharField(max_length=60)
    taken = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.selection_id.name}{self.section}"


class Schedule(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    section_id = models.ForeignKey(SelectionSection, on_delete=models.CASCADE)
    weekday_id = models.ForeignKey(Weekday, on_delete=models.SET_NULL)
    start_time = models.IntegerField(
        default=7, validators=[MinValueValidator("7"), MaxValueValidator("20")]
    )
    end_time = models.IntegerField(
        default=9, validators=[MinValueValidator("9"), MaxValueValidator("22")]
    )

    def __str__(self) -> str:
        return str(self.id)
