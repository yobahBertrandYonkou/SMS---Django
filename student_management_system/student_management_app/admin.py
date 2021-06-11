from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)