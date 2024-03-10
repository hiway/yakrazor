import pytest

from tortoise.exceptions import DoesNotExist

from yakrazor.api import YakrazorAPI


@pytest.fixture
async def api():
    api = YakrazorAPI(database_url="sqlite://:memory:")
    await api.start()
    yield api
    await api.stop()


async def test_create_task(api):
    task = await api.task.create(name="test", status="todo")
    assert task.name == "test"
    assert task.status == "TODO"


async def test_get_task(api):
    task = await api.task.create(name="test", status="todo")
    retrieved_task = await api.task.by_uuid(uuid=task.uuid)
    assert task == retrieved_task


async def test_update_task(api):
    task = await api.task.create(name="test", status="todo")
    updated_task = await api.task.update(uuid=task.uuid, name="test2")
    assert updated_task.name == "test2"


async def test_delete_task(api):
    task = await api.task.create(name="test", status="todo")
    await api.task.delete(uuid=task.uuid)
    with pytest.raises(DoesNotExist):
        await api.task.by_uuid(uuid=task.uuid)


async def test_list_tasks(api):
    task1 = await api.task.create(name="test1", status="todo")
    task2 = await api.task.create(name="test2", status="todo")
    tasks = await api.task.list()
    assert task1 in tasks
    assert task2 in tasks


async def test_filter_tasks_by_status(api):
    task1 = await api.task.create(name="test1", status="todo")
    task2 = await api.task.create(name="test2", status="doing")
    tasks = await api.task.filter_by_status(status="Doing")
    assert task2 in tasks
    assert task1 not in tasks
