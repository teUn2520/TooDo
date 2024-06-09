from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(blank=False, unique=True)

    def __str__(self):
        return f'{self.telegram_id}'


class TelegramTask(models.Model):
    user_id = models.ForeignKey(TelegramUser, to_field='telegram_id', on_delete=models.CASCADE)
    weekday = models.SmallIntegerField(blank=False)
    description = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return f'{self.user_id}'
