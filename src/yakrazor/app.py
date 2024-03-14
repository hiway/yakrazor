from nicegui import app, ui

from yakrazor.api import YakrazorAPI

RAN = False

def run_app():
    global RAN
    if RAN:
        return
    RAN = True
    ui.run()


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
            ui.label("Yakrazor")


api = YakrazorAPI(database_url="sqlite://:memory:")


if __name__ in {"__main__", "__mp_main__", "yakrazor.app"}:
    run_app()
