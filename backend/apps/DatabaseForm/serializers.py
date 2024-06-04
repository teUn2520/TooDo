from rest_framework import serializers

from backend.apps.DatabaseForm.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id']