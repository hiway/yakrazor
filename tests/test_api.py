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
    task = await api.task_create("test")
    assert task.name == "test"
    assert task.done is False


async def test_get_task(api):
    task = await api.task_create("test")
    assert task == await api.task_get(task.uuid)


async def test_list_all_tasks(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    assert [task1, task2] == await api.task_list_all()


async def test_list_todo_tasks(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    assert [task1, task2] == await api.task_list_todo()
    await api.task_update_done(task1.uuid, True)
    assert [task2] == await api.task_list_todo()


async def test_list_done_tasks(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    assert [] == await api.task_list_done()
    await api.task_update_done(task1.uuid, True)
    assert [task1] == await api.task_list_done()


async def test_update_task_name(api):
    task = await api.task_create("test")
    assert task.name == "test"
    task = await api.task_update_name(task.uuid, "new")
    assert task.name == "new"


async def test_update_task_done(api):
    task = await api.task_create("test")
    assert task.done is False
    task = await api.task_update_done(task.uuid, True)
    assert task.done is True


async def test_delete_task(api):
    task = await api.task_create("test")
    await api.task_delete(task.uuid)
    with pytest.raises(DoesNotExist):
        await api.task_get(task.uuid)


async def test_refresh(api):
    refresh_called = False

    def refresh():
        nonlocal refresh_called
        refresh_called = True

    api.refresh_callback = refresh
    await api.refresh()
    assert refresh_called is True
