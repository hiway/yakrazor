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
    ui.run(port=9091, title="Yakrazor", favicon=STATIC / "logo.png")


async def startup():
    await api.start()


async def shutdown():
    await api.stop()


app.on_startup(startup)
app.on_shutdown(shutdown)


@ui.page("/")
async def home():
    with ui.header():
        with ui.row().classes("w-full justify-between items-center"):
            with ui.row().classes("items-center"):
                ui.image(source=STATIC / "logo.png").classes("w-10")
                ui.label("Yakrazor").classes("text-2xl font-bold")
            with ui.button(icon="more_vert").props("flat fab-mini color=white"):
                with ui.menu().classes("w-40"):
                    ui.menu_item("Export").classes("pt-3 h-5")
                    ui.menu_item("Import").classes("pt-3 h-5")
                    ui.separator().classes("h-1")
                    ui.menu_item("Settings").classes("pt-3 h-5")


api = YakrazorAPI(database_url="sqlite://:memory:")


if __name__ in {"__main__", "__mp_main__", "yakrazor.app"}:
    run_app()
