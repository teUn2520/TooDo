from hammett.core import Application, Button
from hammett.core.constants import DEFAULT_STATE, SourcesTypes

from screens.start_screen import HelloScreen
from screens.schedule_screen import ScheduleScreen
from screens.task_input_screen import TaskInputScreen
from states import INPUT_STATE


def main():

    name = 'TooDo'
    app = Application(
        name,
        entry_point=HelloScreen,
        states={
            DEFAULT_STATE: [HelloScreen, ScheduleScreen],
            INPUT_STATE: [TaskInputScreen]
        },
    )
    app.run()


if __name__ == '__main__':
    main()
