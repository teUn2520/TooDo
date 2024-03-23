from hammett.core import Application, Button
from hammett.core.constants import DEFAULT_STATE, SourcesTypes

from screens.start_screen import HelloScreen
from screens.schedule_screen import ScheduleScreen, TaskConfirm, TaskInputScreen
from TooDo.states import INPUT_STATE


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
