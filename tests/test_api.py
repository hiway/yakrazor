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


async def test_create_task_later(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    tasks = await api.task_list_all()
    assert tasks[0] == task1
    assert tasks[1] == task2


async def test_create_task_now(api):
    task1 = await api.task_create("test1", later=False)
    task2 = await api.task_create("test2", later=False)
    tasks = await api.task_list_all()
    assert tasks[0] == task2
    assert tasks[1] == task1


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


async def test_move_up_task(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    await api.task_move_up(task2.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task2
    assert tasks[1] == task1


async def test_move_up_task_first(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    await api.task_move_up(task1.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task1
    assert tasks[1] == task2


async def test_move_down_task(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    await api.task_move_down(task1.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task2
    assert tasks[1] == task1


async def test_move_down_task_last(api):
    task1 = await api.task_create("test1")
    task2 = await api.task_create("test2")
    await api.task_move_down(task2.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task1
    assert tasks[1] == task2


async def test_move_up_task_first_later(api):
    task1 = await api.task_create("test1", later=True)
    task2 = await api.task_create("test2", later=True)
    await api.task_move_up(task1.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task1
    assert tasks[1] == task2
    await api.task_move_up(task2.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task2
    assert tasks[1] == task1


async def test_move_up_task_first_now(api):
    task1 = await api.task_create("test1", later=False)
    task2 = await api.task_create("test2", later=False)
    await api.task_move_up(task1.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task1
    assert tasks[1] == task2
    await api.task_move_up(task2.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task2
    assert tasks[1] == task1


async def test_move_down_task_last_later(api):
    task1 = await api.task_create("test1", later=True)
    task2 = await api.task_create("test2", later=True)
    await api.task_move_down(task2.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task1
    assert tasks[1] == task2
    await api.task_move_down(task1.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task2
    assert tasks[1] == task1


async def test_move_down_task_last_now(api):
    task1 = await api.task_create("test1", later=False)
    task2 = await api.task_create("test2", later=False)
    await api.task_move_down(task2.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task1
    assert tasks[1] == task2
    await api.task_move_down(task1.uuid)
    tasks = await api.task_list_all()
    assert tasks[0] == task2
    assert tasks[1] == task1
