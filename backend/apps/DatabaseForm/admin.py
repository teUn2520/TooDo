from django.contrib import admin

from backend.apps.DatabaseForm.models import TelegramUser, TelegramTask

# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(TelegramTask)