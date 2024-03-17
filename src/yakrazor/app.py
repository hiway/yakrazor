import asyncio
from datetime import datetime
from pathlib import Path

from appdirs import user_data_dir
from nicegui import app, ui
from nicegui.events import GenericEventArguments

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
    await asyncio.sleep(0.2)


app.on_startup(startup)
app.on_shutdown(shutdown)


def today():
    """
    Returns today's date in the format: Saturday, 16 March
    """
    return datetime.now().strftime("%A, %d %B")


@ui.refreshable
async def tasks_list():
    async def toggle_done(task):
        if task.done:
            await api.task_update_done(task.uuid, False)
            await api.task_move_to_top(task.uuid)
        else:
            await api.task_update_done(task.uuid, True)

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
                    done_icon="check"
                    done_color="green"
                else:
                    done_icon="check_box_outline_blank"
                    done_color="primary"
                ui.button(
                    icon=done_icon,
                    color=done_color,
                    on_click=lambda e, task=task: toggle_done(task),
                ).props("dense fab-mini")

                lbl_task_name = ui.label(task.name).classes("flex-grow").props("dense")
                if index == 0:
                    lbl_task_name.classes(add="font-bold")

                with ui.dialog() as dialog, ui.card():
                    txt_task_name = ui.input(
                        value=task.name,
                        on_change=lambda e, task=task: api.task_update_name(
                            task.uuid, e.value
                        ),
                    )
                    ui.button("Save", on_click=lambda: (dialog.close(), tasks_list.refresh()))

                with ui.button(icon="more_vert").props(
                    "flat fab-mini color=grey dense"
                ):
                    with ui.menu().classes("w-40"):
                        ui.menu_item(
                            "Edit",
                            on_click=lambda e, task=task, dialog=dialog: dialog.open(),
                        ).classes("pt-3 h-5")
                        ui.separator().classes("h-1")
                        ui.menu_item(
                            "Move up",
                            on_click=lambda e, task=task: api.task_move_up(task.uuid),
                        ).classes("pt-3 h-5")
                        ui.menu_item(
                            "Move down",
                            on_click=lambda e, task=task: api.task_move_down(task.uuid),
                        ).classes("pt-3 h-5")
                        ui.menu_item(
                            "Move to top",
                            on_click=lambda e, task=task: api.task_move_to_top(
                                task.uuid
                            ),
                        ).classes("pt-3 h-5")
                        ui.menu_item(
                            "Move to bottom",
                            on_click=lambda e, task=task: api.task_move_to_bottom(
                                task.uuid
                            ),
                        ).classes("pt-3 h-5")
                        ui.separator().classes("h-1")
                        ui.menu_item(
                            "Delete",
                            on_click=lambda e, task=task: api.task_delete(task.uuid),
                        ).classes("pt-3 h-5")


@ui.page("/")
async def home():
    async def create_task_now(e: GenericEventArguments):
        if e.args["shiftKey"] is True:
            return
        await api.task_create(txt_task.value, later=False)
        txt_task.set_value("")

    async def create_task_later(e: GenericEventArguments):
        await api.task_create(txt_task.value, later=True)
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
            txt_task.on("keydown.shift.enter", create_task_later)
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
