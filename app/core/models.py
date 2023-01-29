from django.contrib.auth.models import BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create(self, first_name, last_name, username, email, password):
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
    ):
        user = self.create(first_name, last_name, username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

    def normalize_email(self, email: str):
        return email.lower()
