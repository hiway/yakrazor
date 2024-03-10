import datetime
from dataclasses import dataclass

from yakrazor import database
from yakrazor.models import Task, TaskStatus


@dataclass
class YakrazorAPI:
    """
    YakrazorAPI
    -----------
    """

    database_url: str

    async def start(self) -> None:
        await database.open(self.database_url)

    async def stop(self) -> None:
        await database.close()

    async def create_task(self, name: str, status: str) -> dict:
        task = await Task.create(
            name=name,
            status_value=TaskStatus[status.upper()],
        )
        return task

    async def get_task(self, uuid: str) -> dict:
        task = await Task.get(uuid=uuid)
        return task

    async def update_task(
        self, uuid: str, name: str = None, status: str = None
    ) -> dict:
        task = await Task.get(uuid=uuid)
        if name:
            task.name = name
        if status:
            task.status_value = TaskStatus[status.upper()]
            task.status_changed_at = datetime.datetime.now(datetime.UTC)
        await task.save()
        return task

    async def delete_task(self, uuid: str) -> None:
        task = await Task.get(uuid=uuid)
        await task.delete()

    async def list_tasks(self) -> list:
        tasks = await Task.all()
        return tasks

    async def filter_tasks_by_status(self, status: str) -> list:
        tasks = await Task.filter(status_value=TaskStatus[status.upper()])
        return tasks
