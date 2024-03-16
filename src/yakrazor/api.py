import datetime
from dataclasses import dataclass
from typing import List, Optional

from yakrazor import database
from yakrazor.models import Task


@dataclass
class YakrazorAPI:
    """
    YakrazorAPI
    -----------
    """

    database_url: str
    refresh_callback: Optional[callable] = None

    async def start(self) -> None:
        await database.open(self.database_url)

    async def stop(self) -> None:
        await database.close()

    async def refresh(self) -> None:
        if self.refresh_callback:
            self.refresh_callback()

    async def task_create(self, name: str, later: bool = True) -> Task:
        if later:
            tasks = await Task.all().order_by("-order")
        else:
            tasks = await Task.all().order_by("order")

        if tasks:
            if later:
                order = tasks[0].order + 1
            else:
                order = tasks[0].order - 1
        else:
            order = 0
        task = await Task.create(name=name, order=order)
        await self.refresh()
        return task

    async def task_get(self, uuid: str) -> Task:
        task = await Task.get(uuid=uuid)
        return task

    async def task_list_all(self) -> List[Task]:
        task = await Task.all().order_by("order")
        return task

    async def task_list_todo(self) -> List[Task]:
        task_list = await Task.filter(done=False).order_by("order")
        return task_list

    async def task_list_done(self) -> List[Task]:
        task_list = await Task.filter(done=True).order_by("order")
        return task_list

    async def task_update_name(self, uuid: str, name: str) -> Task:
        task = await Task.get(uuid=uuid)
        task.name = name
        await task.save()
        return task

    async def task_update_done(self, uuid: str, done: bool) -> Task:
        task = await Task.get(uuid=uuid)
        task.done = done
        await task.save()
        await self.refresh()
        return task

    async def task_delete(self, uuid: str) -> None:
        task = await Task.get(uuid=uuid)
        await task.delete()
        await self.refresh()

    async def task_move_up(self, uuid: str) -> None:
        task = await Task.get_or_none(uuid=uuid)
        if task:
            tasks = await Task.filter(order__lt=task.order).order_by("-order").limit(1)
            if tasks:
                higher_task = tasks[0]
                task.order, higher_task.order = higher_task.order, task.order
                await task.save()
                await higher_task.save()
        await self.refresh()

    async def task_move_down(self, uuid: str) -> None:
        task = await Task.get_or_none(uuid=uuid)
        if task:
            tasks = await Task.filter(order__gt=task.order).order_by("order").limit(1)
            if tasks:
                lower_task = tasks[0]
                task.order, lower_task.order = lower_task.order, task.order
                await task.save()
                await lower_task.save()
        await self.refresh()
