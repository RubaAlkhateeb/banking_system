from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(max_length=200, blank=False, validators=[EmailValidator()], unique=True)
    password = models.CharField(max_length=30, blank= False)
    phone = models.CharField(max_length=30, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.username


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iban = models.CharField(max_length=24, blank=False)
    account_number = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(999999999999),
            MinValueValidator(1)
        ],
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return f"Account for {self.user.username}"