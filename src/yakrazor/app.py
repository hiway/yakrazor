from datetime import datetime
from pathlib import Path

from appdirs import user_data_dir
from nicegui import app, ui

from yakrazor.api import YakrazorAPI

RAN = False
STATIC = Path(__file__).parent / "static"
DATA_DIR = Path(user_data_dir("yakrazor"))


def run_app():
    global RAN
    if RAN:
        return
    RAN = True
    ui.run(port=9090, title="Yakrazor", favicon=STATIC / "logo.png")


async def startup():
    await api.start()


async def shutdown():
    await api.stop()


app.on_startup(startup)
app.on_shutdown(shutdown)


def today():
    """
    Returns today's date in the format: Saturday, 16 March
    """
    return datetime.now().strftime("%A, %d %B")


@ui.refreshable
async def tasks_list():
    tasks_all = await api.task_list_all()
    tasks_todo = await api.task_list_todo()
    tasks_done = await api.task_list_done()
    if len(tasks_all) == 0:
        badge_text = f"Nothing to do!"
        badge_completed = ui.badge(badge_text, color="primary").props("floating")
        with ui.row().classes("items-center w-full"):
            ui.label("Type something in the box above and press enter").classes(
                "flex-grow p-6 text-center"
            )
    else:
        badge_text = f"{len(tasks_done)} of {len(tasks_all)} done"
        badge_color = "green" if len(tasks_done) == len(tasks_all) else "primary"
        badge_completed = ui.badge(badge_text, color=badge_color).props("floating")

        for index, task in enumerate(tasks_todo + tasks_done):
            with ui.row().classes("items-center w-full"):
                if task.done:
                    ui.button(
                        icon="check",
                        color="green",
                        on_click=lambda e, task=task: api.task_update_done(
                            task.uuid, False
                        ),
                    ).props("dense fab-mini")
                else:
                    ui.button(
                        icon="check_box_outline_blank",
                        on_click=lambda e, task=task: api.task_update_done(
                            task.uuid, True
                        ),
                    ).props("dense fab-mini")
                if index == 0:
                    txt_task_name = (
                        ui.input(
                            on_change=lambda e, task=task: api.task_update_name(
                                task.uuid, txt_task_name.value
                            ),
                            value=task.name,
                        )
                        .classes("flex-grow font-bold")
                        .props("dense input-style='font-weight: bold;'")
                    )
                else:
                    txt_task_name = (
                        ui.input(
                            on_change=lambda e, task=task: api.task_update_name(
                                task.uuid, txt_task_name.value
                            ),
                            value=task.name,
                        )
                        .classes("flex-grow")
                        .props("dense")
                    )

                with ui.button(icon="more_vert").props(
                    "flat fab-mini color=grey dense"
                ):
                    with ui.menu().classes("w-40"):
                        ui.menu_item(
                            "Move up",
                            on_click=lambda e, task=task: api.task_move_up(task.uuid),
                        ).classes("pt-3 h-5")
                        ui.menu_item(
                            "Move down",
                            on_click=lambda e, task=task: api.task_move_down(task.uuid),
                        ).classes("h-5")
                        ui.menu_item(
                            "Delete",
                            on_click=lambda e, task=task: api.task_delete(task.uuid),
                        ).classes("pt-3 h-5")


@ui.page("/")
async def home():
    async def create_task_now():
        await api.task_create(txt_task.value, later=False)
        txt_task.set_value("")

    with ui.header().classes("w-full justify-between items-center"):
        with ui.row().classes("items-center"):
            ui.image(source=STATIC / "logo.png").classes("w-10")
            ui.label("Yakrazor").classes("text-2xl font-bold")

    with ui.card().classes("w-full"):
        badge_date = ui.badge(today(), color="secondary").props("floating")
        with ui.row().classes("w-full"):
            txt_task = (
                ui.input(placeholder="Get this done...")
                .classes("flex-grow")
                .props("dense")
            )
            txt_task.on("keydown.enter", create_task_now)

    with ui.card().classes("w-full"):
        await tasks_list()


DATA_DIR.mkdir(parents=True, exist_ok=True)
print(f"Using data directory: {DATA_DIR}")

api = YakrazorAPI(
    database_url=f"sqlite://{DATA_DIR / 'yakrazor.db'}",
    refresh_callback=tasks_list.refresh,
)


if __name__ in {"__main__", "__mp_main__", "yakrazor.app"}:
    run_app()
