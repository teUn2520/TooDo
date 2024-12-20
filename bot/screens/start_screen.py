from hammett.core import Button
from hammett.core.handlers import register_button_handler
from hammett.core.mixins import StartMixin
from hammett.conf import settings
import httpx

from bot.screens.schedule_screen import ScheduleScreen


class HelloScreen(StartMixin):
    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = 'Привет, я твой персональный помощник.'

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button('Планировать ⏰',
                   self.go_to_schedule_screen)
        ]]

    @register_button_handler
    async def go_to_schedule_screen(self, update, context):
        user_data = update.effective_user
        response = httpx.get('http://127.0.0.1:8000/api/telegramuser/')
        response = response.json()
        for aut_user in response:
            if aut_user['telegram_id'] == user_data.id:
                return await ScheduleScreen().goto(update, context)

        httpx.post('http://127.0.0.1:8000/api/telegramuser/', data={'telegram_id': user_data.id})

        return await ScheduleScreen().goto(update, context)
