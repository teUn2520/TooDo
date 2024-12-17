from hammett.core import Button, Screen
from hammett.core.constants import SourcesTypes, RenderConfig, DEFAULT_STATE
from hammett.core.handlers import register_button_handler, register_typing_handler
from hammett.core.mixins import StartMixin, RouteMixin
from hammett.conf import settings
import httpx

from bot.states import INPUT_STATE, DELETE_STATE, SEARCH_STATE

DAYS_WEEK = ("Понедельник", "Вторник", "Среда", "Четверг",
             "Пятница", "Суббота", "Воскресенье")


async def days_week_dynamic_keyboard(handler):
    return [
        [Button(
            weekday,
            handler,
            source_type=SourcesTypes.HANDLER_SOURCE_TYPE,
            payload={num: weekday}
        )]
        for num, weekday in enumerate(DAYS_WEEK)
    ]


class ScheduleScreen(StartMixin, Screen):
    cover = settings.MEDIA_ROOT / 'planner.jpg'
    description = ('Чтобы добавить новую задачу выбери день недели, а после введи то, что хочешь запланировать.'
                   '\n\n'
                   '<b>Твое раписание:</b>\n')

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button("Новая задача",
                   self.new_task),
            Button("Удалить задачу",
                   self.delete_task),
            Button("Найти задачу",
                   self.search_task),
        ]]

    @register_button_handler
    async def new_task(self, update, context):
        return await TaskDayChoiceScreen().goto(update, context)

    @register_button_handler
    async def delete_task(self, update, context):
        return await TaskDeleteInputScreen().sgoto(update, context)

    @register_button_handler
    async def search_task(self, update, context):
        return await TaskSearchInputScreen().sgoto(update, context)

    async def get_config(self, update, context, **kwargs):
        current_description = await self.get_description(update, context)
        response = httpx.get('http://127.0.0.1:8000/api/telegramtask/')
        response = response.json()

        user_data = update.effective_user

        for task in response:
            if task['user_id'] == user_data.id:
                for num, weekday in enumerate(DAYS_WEEK):
                    if task['weekday'] == num:
                        temp_description = f"{weekday}: {task['description']}\n"
                        current_description += temp_description

        return RenderConfig(description=current_description)


class TaskSearchInputScreen(RouteMixin, Screen):
    routes = (
        ({DEFAULT_STATE}, SEARCH_STATE),
    )
    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = "Напиши день недели или задачу, которую хочешь найти.\n"

    @register_typing_handler
    async def user_search_input(self, update, context):
        user_task_search_text = update.message.text
        context.user_data['user_task_search_text'] = user_task_search_text

        return await TaskSearchingScreen().sjump(update, context)


class TaskSearchingScreen(RouteMixin, Screen):
    routes = (
        ({SEARCH_STATE}, DEFAULT_STATE),
    )
    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = "Найденные задачи:\n"

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button("Назад",
                   ScheduleScreen,
                   source_type=SourcesTypes.GOTO_SOURCE_TYPE),
        ]]

    async def get_config(self, update, context, **kwargs):
        current_description = await self.get_description(update, context)
        response = httpx.get('http://127.0.0.1:8000/api/telegramtask/')
        response = response.json()
        user_data = update.effective_user

        for task in response:
            if task['user_id'] == user_data.id:
                for num, weekday in enumerate(DAYS_WEEK):
                    if context.user_data['user_task_search_text'] == weekday:
                        if task['weekday'] == num:
                            current_description += f"{weekday}: {task['description']}\n"
                    if context.user_data['user_task_search_text'] in task['description'] and num == task['weekday']:
                        current_description += f"{weekday}: {task['description']}\n"

        return RenderConfig(description=current_description)


class TaskDeleteInputScreen(RouteMixin, Screen):
    routes = (
        ({DEFAULT_STATE}, DELETE_STATE),
    )
    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = "Напиши задачу, которую хочешь удалить.\n"

    async def get_config(self, update, context, **kwargs):
        current_description = await self.get_description(update, context)
        response = httpx.get('http://127.0.0.1:8000/api/telegramtask/')
        response = response.json()

        user_data = update.effective_user

        for task in response:
            if task['user_id'] == user_data.id:
                for num, weekday in enumerate(DAYS_WEEK):
                    if task['weekday'] == num:
                        temp_description = f"{weekday}: {task['description']}\n"
                        current_description += temp_description

        return RenderConfig(description=current_description)

    @register_typing_handler
    async def user_to_delete_input(self, update, context):
        user_task_delete_text = update.message.text
        context.user_data['user_task_delete_text'] = user_task_delete_text

        return await TaskDeleteConfirmScreen().sjump(update, context)


class TaskDeleteConfirmScreen(RouteMixin, Screen):
    routes = (
        ({DELETE_STATE}, DEFAULT_STATE),
    )
    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = "Вы уверены, что хотите удалить задачу:\n"

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button("Удалить",
                   self.delete_current_task),
            Button("Назад",
                   self.back_to_delete_input),
        ]]

    async def get_config(self, update, context, **kwargs):
        current_description = await self.get_description(update, context)
        response = httpx.get('http://127.0.0.1:8000/api/telegramtask/')
        response = response.json()

        user_data = update.effective_user

        for task in response:
            if task['user_id'] == user_data.id:
                if context.user_data['user_task_delete_text'] in task['description']:
                    temp_description = task['description']
                    current_description += temp_description

        return RenderConfig(description=current_description)

    @register_button_handler
    async def delete_current_task(self, update, context):
        response = httpx.get('http://127.0.0.1:8000/api/telegramtask/')
        response = response.json()

        user_data = update.effective_user

        for task in response:
            if task['user_id'] == user_data.id:
                if context.user_data['user_task_delete_text'] in task['description']:
                    task_to_delete = 'http://127.0.0.1:8000/api/telegramtask/' + str(task['id']) + "/"
                    httpx.delete(task_to_delete)
                    break

        return await ScheduleScreen().goto(update, context)

    @register_button_handler
    async def back_to_delete_input(self, update, context):
        return await TaskDeleteInputScreen().sgoto(update, context)


class TaskDayChoiceScreen(RouteMixin, Screen):
    routes = (
        ({INPUT_STATE}, DEFAULT_STATE),
    )
    cover = settings.MEDIA_ROOT / 'toodo.png'
    description = "Выбери день на который хочешь установить задачу."

    async def get_config(self, update, context, **kwargs):
        keyboard = await days_week_dynamic_keyboard(self.weekday_catcher)

        return RenderConfig(keyboard=keyboard)

    @register_button_handler
    async def weekday_catcher(self, update, context):
        payload = await self.get_payload(update, context)
        for day_num in range(7):
            try:
                context.user_data['user_day_choice'] = payload[day_num]
                context.user_data['user_weekday_id'] = day_num
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
                   TaskDayChoiceScreen,
                   source_type=SourcesTypes.SGOTO_SOURCE_TYPE)
        ]]

    @register_typing_handler
    async def user_input_catcher(self, update, context):
        user_input_text = update.message.text

        context.user_data['user_task'] = user_input_text

        return await TaskConfirmScreen().sjump(update, context)


class TaskConfirmScreen(RouteMixin, Screen):
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
                "Создать задачу сначала",
                self.retask,
            )],
            [Button(
                "Все верно",
                self.task_confirm,
            )]
        ]

        return RenderConfig(description=description, keyboard=keyboard)

    @register_button_handler
    async def retask(self, update, context):
        return await ScheduleScreen().goto(update, context)

    @register_button_handler
    async def task_confirm(self, update, context):
        user_task = context.user_data['user_task']
        user_weekday_id = context.user_data['user_weekday_id']
        user_data = update.effective_user

        data = {'user_id': user_data.id, 'weekday': user_weekday_id, 'description': user_task}
        httpx.post('http://127.0.0.1:8000/api/telegramtask/', data=data)

        return await ScheduleScreen().goto(update, context)
