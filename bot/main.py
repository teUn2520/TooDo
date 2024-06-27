from hammett.core import Application
from hammett.core.constants import DEFAULT_STATE

from screens.start_screen import HelloScreen
from screens.schedule_screen import (ScheduleScreen, TaskInputScreen, TaskConfirm,
                                     TaskDayChoiceScreen, TaskDeleteScreen, TaskDeleteConfirmScreen)
from states import INPUT_STATE, DELETE_STATE


def main():

    name = 'TooDo'
    app = Application(
        name,
        entry_point=HelloScreen,
        states={
            DEFAULT_STATE: [HelloScreen, ScheduleScreen, TaskConfirm, TaskDayChoiceScreen, TaskDeleteConfirmScreen],
            INPUT_STATE: [TaskInputScreen],
            DELETE_STATE: [TaskDeleteScreen],
        },
    )
    app.run()


if __name__ == '__main__':
    main()
