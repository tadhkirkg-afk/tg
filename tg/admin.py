from django.contrib import admin
from .models import TelegramUser, Wait


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "gender")

@admin.register(Wait)
class WaitAdmin(admin.ModelAdmin):
    list_display = ("id", "user")