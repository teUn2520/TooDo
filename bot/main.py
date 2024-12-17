from hammett.core import Application
from hammett.core.constants import DEFAULT_STATE

from screens.start_screen import HelloScreen
from screens.schedule_screen import (ScheduleScreen, TaskInputScreen, TaskConfirmScreen,
                                     TaskDayChoiceScreen, TaskDeleteInputScreen, TaskDeleteConfirmScreen,
                                     TaskSearchInputScreen, TaskSearchingScreen)
from states import INPUT_STATE, DELETE_STATE, SEARCH_STATE


def main():

    name = 'TooDo'
    app = Application(
        name,
        entry_point=HelloScreen,
        states={
            DEFAULT_STATE: [HelloScreen, ScheduleScreen, TaskConfirmScreen,
                            TaskDayChoiceScreen, TaskDeleteConfirmScreen, TaskSearchingScreen],
            INPUT_STATE: [TaskInputScreen],
            DELETE_STATE: [TaskDeleteInputScreen],
            SEARCH_STATE: [TaskSearchInputScreen],
        },
    )
    app.run()


if __name__ == '__main__':
    main()
