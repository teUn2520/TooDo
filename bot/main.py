from hammett.core import Application
from hammett.core.constants import DEFAULT_STATE

from screens.start_screen import HelloScreen
from screens.schedule_screen import ScheduleScreen, TaskInputScreen, TaskConfirm
from states import INPUT_STATE


def main():

    name = 'TooDo'
    app = Application(
        name,
        entry_point=HelloScreen,
        states={
            DEFAULT_STATE: [HelloScreen, ScheduleScreen, TaskConfirm],
            INPUT_STATE: [TaskInputScreen],
        },
    )
    app.run()


if __name__ == '__main__':
    main()
