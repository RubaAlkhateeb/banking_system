from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=200, blank=False)
    password = models.CharField(max_length=30, blank= False)
    phone = models.CharField(max_length=30, blank=False)
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

    def __str__(self):
        return self.user_name
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)