from django.contrib import admin
from .models import User, UserAccount

# Register your models here.
admin.site.register(User)
admin.site.register(UserAccount)