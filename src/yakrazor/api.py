import datetime
from dataclasses import dataclass
from typing import List

from yakrazor import database
from yakrazor.models import Task, TaskStatus


class TasksAPI:
    async def create(self, name: str, status: str) -> Task:
        task = await Task.create(
            name=name,
            status_value=TaskStatus[status.upper()],
        )
        return task

    async def get(self, uuid: str) -> Task:
        task = await Task.get(uuid=uuid)
        return task

    async def update(self, uuid: str, name: str = None, status: str = None) -> Task:
        task = await Task.get(uuid=uuid)
        if name:
            task.name = name
        if status:
            task.status_value = TaskStatus[status.upper()]
            task.status_changed_at = datetime.datetime.now(datetime.UTC)
        await task.save()
        return task

    async def delete(self, uuid: str) -> None:
        task = await Task.get(uuid=uuid)
        await task.delete()

    async def all(self) -> List[Task]:
        tasks = await Task.all()
        return tasks

    async def filter_by_status(self, status: str) -> List[Task]:
        tasks = await Task.filter(status_value=TaskStatus[status.upper()])
        return tasks


@dataclass
class YakrazorAPI:
    """
    YakrazorAPI
    -----------
    """

    database_url: str
    task: TasksAPI = TasksAPI()

    async def start(self) -> None:
        await database.open(self.database_url)

    async def stop(self) -> None:
        await database.close()
