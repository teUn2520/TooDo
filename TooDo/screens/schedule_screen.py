from hammett.core import Button, Screen
from hammett.core.constants import SourcesTypes, RenderConfig, DEFAULT_STATE, EMPTY_KEYBOARD
from hammett.core.handlers import (
    register_button_handler,
    register_typing_handler,
)
from hammett.core.screen import StartScreen, RouteMixin
from hammett.conf import settings
from telegram.ext import filters

from TooDo.states import INPUT_STATE


async def days_week_dynamic_keyboard(handler):
    days_week = ("Понедельник", "Вторник", "Среда", "Четверг",
                 "Пятница", "Суббота", "Воскресенье")

    return [
        [Button(
            day,
            handler,
            source_type=SourcesTypes.HANDLER_SOURCE_TYPE,
            payload=day
        )]
        for day in days_week
    ]


class ScheduleScreen(StartScreen):
    routes = (
        ({DEFAULT_STATE}, INPUT_STATE),
    )

    cover = settings.MEDIA_ROOT / 'planner.jpg'
    description = ('<b>Твое раписание: </b> \n\n\n '
                   'Чтобы добавить задачу выбери определенный день '
                   'недели и введи задачу, которую нужно добавить')

    async def get_config(self, update, context, **kwargs):
        keyboard = await days_week_dynamic_keyboard(self.handle_button_click)
        return RenderConfig(keyboard=keyboard)

    @register_button_handler
    async def handle_button_click(self, update, context):
        payload = await self.get_payload(update, context)

        context.user_data['day_choice'] = payload

        return await TaskInputScreen().sgoto(update, context)


class TaskInputScreen(RouteMixin, Screen):
    routes = (
        ({DEFAULT_STATE}, INPUT_STATE),
    )

    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = "Теперь поставь задачу, просто напиши в чат и я добавлю ее в твое расписание."

    @register_typing_handler
    async def handle_task_input(self, update, context):
        task_text = update.message.text
        print(task_text)
        context.user_data['user_task'] = task_text

        return await TaskConfirm().sjump(update, context)


class TaskConfirm(RouteMixin, Screen):
    routes = (
        ({INPUT_STATE}, DEFAULT_STATE),
    )

    async def get_config(self, update, context):
        user_task = context.user_data['user_task']
        user_day = context.user_data['day_choice']
        description = f"Ваша задача {user_task} установлена на {user_day}"
        keyboard = [
                [Button(
                    "Создать задачу сначала.",
                    ScheduleScreen,
                    source_type=SourcesTypes.GOTO_SOURCE_TYPE,
                )],
                [Button(
                    "Все верно.",
                    self.handle_task_create,
                    source_type=SourcesTypes.HANDLER_SOURCE_TYPE
                )]
            ]

        return RenderConfig(description=description, keyboard=keyboard)

    @register_button_handler
    async def handle_task_create(self, update, context):
        pass
