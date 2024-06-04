from hammett.core import Button
from hammett.core.constants import SourcesTypes
from hammett.core.mixins import StartMixin
from hammett.conf import settings

from bot.screens.schedule_screen import ScheduleScreen


class HelloScreen(StartMixin):
    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = 'Привет, я твой персональный помощник.'

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button('Планировать ⏰',
                   ScheduleScreen,
                   source_type=SourcesTypes.GOTO_SOURCE_TYPE)
        ]]
