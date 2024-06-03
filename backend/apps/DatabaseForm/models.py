from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(blank=False)


class TelegramTask(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    weekday = models.SmallIntegerField(blank=False)
    description = models.CharField(max_length=1000, blank=False)
