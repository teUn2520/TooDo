from hammett.core import Button, Screen
from hammett.core.constants import SourcesTypes, RenderConfig, DEFAULT_STATE
from hammett.core.handlers import register_button_handler, register_typing_handler
from hammett.core.mixins import StartMixin, RouteMixin
from hammett.conf import settings
import httpx
import json

from bot.states import INPUT_STATE


async def days_week_dynamic_keyboard(handler):
    days_week = ("Понедельник", "Вторник", "Среда", "Четверг",
                 "Пятница", "Суббота", "Воскресенье")

    return [
        [Button(
            weekday,
            handler,
            source_type=SourcesTypes.HANDLER_SOURCE_TYPE,
            payload={num: weekday}
        )]
        for num, weekday in enumerate(days_week)
    ]


async def schedule_dynamic_description(context):
    user_task = context.user_data['user_task']
    user_day_choice = context.user_data['user_day_choice']

    description = f"{user_day_choice}: {user_task}\n"

    return description


class ScheduleScreen(RouteMixin, StartMixin):
    routes = (
        ({INPUT_STATE}, DEFAULT_STATE),
    )

    cover = settings.MEDIA_ROOT / 'planner.jpg'
    description = ('Чтобы добавить новую задачу выбери день недели, а после введи то, что хочешь запланировать.'
                   '\n\n'
                   '<b>Твое раписание:</b>\n')

    async def get_config(self, update, context, **kwargs):
        try:
            keyboard = await days_week_dynamic_keyboard(self.weekday_catcher)
            current_description = await self.get_description(update, context)
            additional_description = await schedule_dynamic_description(context)
            description = current_description + additional_description

            return RenderConfig(description=description, keyboard=keyboard)

        except KeyError:
            return RenderConfig(keyboard=keyboard)

    @register_button_handler
    async def weekday_catcher(self, update, context):
        payload = await self.get_payload(update, context)
        for num in range(6):
            try:
                context.user_data['user_day_choice'] = payload[num]
                context.user_data['user_weekday_id'] = num
            except KeyError:
                continue

        return await TaskInputScreen().sgoto(update, context)


class TaskInputScreen(RouteMixin, Screen):
    routes = (
        ({DEFAULT_STATE}, INPUT_STATE),
    )

    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = "Теперь поставь задачу, просто напиши в чат и я добавлю ее в твое расписание."

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button('Назад',
                   ScheduleScreen,
                   source_type=SourcesTypes.SGOTO_SOURCE_TYPE)
        ]]

    @register_typing_handler
    async def user_input_catcher(self, update, context):
        user_input_text = update.message.text

        context.user_data['user_task'] = user_input_text

        return await TaskConfirm().sjump(update, context)


class TaskConfirm(RouteMixin, Screen):
    routes = (
        ({INPUT_STATE}, DEFAULT_STATE),
    )

    cover = settings.MEDIA_ROOT / 'toodo.png'

    async def get_config(self, update, context, **kwargs):
        user_task = context.user_data['user_task']
        user_day_choice = context.user_data['user_day_choice']
        description = f"Ваша задача {user_task} установлена на {user_day_choice}"
        keyboard = [
            [Button(
                "Создать задачу сначала.",
                self.retask,
            )],
            [Button(
                "Все верно.",
                self.task_confirm,
            )]
        ]

        return RenderConfig(description=description, keyboard=keyboard)

    @register_button_handler
    async def retask(self, update, context):
        context.user_data.pop('user_task')
        context.user_data.pop('user_day_choice')
        context.user_data.pop('user_weekday_id')

        return await ScheduleScreen().sgoto(update, context)

    @register_button_handler
    async def task_confirm(self, update, context):
        user_task = context.user_data['user_task']
        user_weekday_id = context.user_data['user_weekday_id']
        user_data = update.effective_user

        data = {'user_id': user_data.id, 'weekday': user_weekday_id, 'description': user_task}

        response = await httpx.post('http://127.0.0.1:8000/api/telegramtask/', data=data)

        return ScheduleScreen().sgoto(update, context)
