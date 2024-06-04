from rest_framework import viewsets

from backend.apps.DatabaseForm.models import TelegramUser, TelegramTask
from backend.apps.DatabaseForm.serializers import TelegramUserSerializer, TelegramTaskSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer


class TelegramTaskViewSet(viewsets.ModelViewSet):
    queryset = TelegramTask.objects.all()
    serializer_class = TelegramTaskSerializer
