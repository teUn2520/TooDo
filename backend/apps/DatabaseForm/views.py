from rest_framework import viewsets

from backend.apps.DatabaseForm.models import TelegramUser
from backend.apps.DatabaseForm.serializers import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):

    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
