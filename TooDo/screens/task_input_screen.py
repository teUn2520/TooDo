from hammett.core.constants import EMPTY_KEYBOARD

from screens.schedule_screen import ScheduleScreen


class TaskInputScreen(ScheduleScreen):
    description = "Теперь поставь задачу, просто напиши в чат и я добавлю ее в твое расписание."
    keyboard = EMPTY_KEYBOARD
