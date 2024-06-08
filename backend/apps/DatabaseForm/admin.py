from django.contrib import admin

from backend.apps.DatabaseForm.models import TelegramUser, TelegramTask


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Представление модели TelegramUser в панели администратора."""


@admin.register(TelegramTask)
class TelegramTaskAdmin(admin.ModelAdmin):
    """Представление модели TelegramTask в панели администратора."""
