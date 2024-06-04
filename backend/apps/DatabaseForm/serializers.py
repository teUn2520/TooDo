from rest_framework import serializers

from backend.apps.DatabaseForm.models import TelegramUser, TelegramTask


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id']


class TelegramTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramTask
        fields = ['user', 'weekday', 'description']