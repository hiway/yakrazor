from pathlib import Path

from nicegui import app, ui

from yakrazor.api import YakrazorAPI

RAN = False
STATIC = Path(__file__).parent / "static"


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


@ui.page("/")
async def home():
    with ui.header().classes("w-full justify-between items-center"):
        with ui.row().classes("items-center"):
            ui.image(source=STATIC / "logo.png").classes("w-10")
            ui.label("Yakrazor").classes("text-2xl font-bold")

        with ui.button(icon="menu").props("flat fab-mini color=white"):
            with ui.menu().classes("w-40"):
                ui.menu_item("Export").classes("pt-3 h-5")
                ui.menu_item("Import").classes("pt-3 h-5")
                ui.separator().classes("h-1")
                ui.menu_item("Settings").classes("pt-3 h-5")
 
    with ui.card().classes("w-full"):
        badge_date = ui.badge('Saturday, 16 March', color='secondary').props('floating')
        with ui.row().classes("w-full"):
            ui.select(["Chores", "Shopping", "Work", "Personal"], value="Chores").classes("flex-grow").props("dense")
            with ui.button(icon="more_vert").props("flat fab-mini color=grey dense"):
                with ui.menu().classes("w-40"):
                    ui.menu_item("Clear All Tasks").classes("pt-3 h-5")
                    ui.separator()
                    ui.menu_item("New Project").classes("pt-3 h-5")
                    ui.menu_item("Delete Project").classes("pt-3 h-5")
        
        with ui.row().classes("w-full"):
            ui.input(placeholder="Get this done...").classes("flex-grow").props("dense")
            with ui.button(icon="add").props("flat fab-mini color=grey dense"):
                with ui.menu().classes("w-40"):
                    ui.menu_item("Now").classes("pt-3 h-5")
                    ui.menu_item("Today").classes("pt-3 h-5")
                    ui.menu_item("Tomorrow").classes("pt-3 h-5")
                    ui.menu_item("Later").classes("pt-3 h-5")

    with ui.card().classes("w-full"):
        badge_completed = ui.badge('0 of 7 completed', color='primary').props('floating')
        for index in range(7):
            with ui.row().classes("items-center w-full"):
                ui.checkbox().props("dense")
                ui.label(f"Task {index + 1}").classes("flex-grow font-bold").props("dense")
                with ui.button(icon="more_vert").props("flat fab-mini color=grey dense"):
                    with ui.menu():
                        ui.menu_item("Move up").classes("pt-3 h-5")
                        ui.menu_item("Move down").classes("pt-3 h-5")
            ui.separator()



api = YakrazorAPI(database_url="sqlite://:memory:")


if __name__ in {"__main__", "__mp_main__", "yakrazor.app"}:
    run_app()