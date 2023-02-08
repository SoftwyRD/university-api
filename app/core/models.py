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
from uuid import uuid4

# Create your models here.


class UserManager(BaseUserManager):
    def create(
        self,
        first_name,
        last_name,
        username,
        email,
        password,
        middle_name=None,
    ) -> User:
        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        first_name,
        last_name,
        username,
        email,
        password,
        middle_name=None,
    ) -> User:
        user = self.create(
            first_name, last_name, username, email, password, middle_name
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

        return user

    def normalize_email(self, email: str):
        return email.lower()


class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50)
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator],
    )
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self) -> str:
        return self.username


class Subject(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    code = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=255, unique=True)
    credits = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_lab = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id} - {self.code} - {self.name}"

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class Weekday(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.name


class Selection(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, unique=True, editable=False
    )
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        ret = f"{self.name} + {self.id} + {self.user}"
        return ret


class SubjectSection(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    selection = models.ForeignKey(
        Selection, on_delete=models.SET_NULL, null=True
    )
    section = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    professor = models.CharField(max_length=60)
    taken = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.selection.name}{self.section}"


class SectionSchedule(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    section = models.ForeignKey(SubjectSection, on_delete=models.CASCADE)
    weekday = models.ForeignKey(Weekday, on_delete=models.SET_NULL, null=True)
    start_time = models.IntegerField(
        default=7, validators=[MinValueValidator(7), MaxValueValidator(20)]
    )
    end_time = models.IntegerField(
        default=9, validators=[MinValueValidator(9), MaxValueValidator(22)]
    )

    def __str__(self) -> str:
        return str(self.id)
