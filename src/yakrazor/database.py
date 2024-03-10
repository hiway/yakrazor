from tortoise import Tortoise, connections

MODELS = [
    "yakrazor.models.task",
]


async def open(db_url: str) -> None:
    await Tortoise.init(db_url=db_url, modules=dict(yakrazor=MODELS))
    await Tortoise.generate_schemas()


async def close() -> None:
    await connections.close_all()
