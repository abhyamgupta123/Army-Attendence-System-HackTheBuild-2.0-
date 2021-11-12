from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTable(admin.ModelAdmin):
    list_display = ("user", "uid")

admin.site.register(UserProfile, UserProfileTable)
