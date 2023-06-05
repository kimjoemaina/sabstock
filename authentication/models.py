from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password, name=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email