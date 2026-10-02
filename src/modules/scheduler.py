import asyncio
from asyncio import PriorityQueue
from typing import TYPE_CHECKING, cast

from db.tasks import find_many
from shared.clock import utc_now

if TYPE_CHECKING:
    from _typing import TaskCallback
    from datetime import datetime

    from db._typing import Task


pq: PriorityQueue[tuple[datetime, Task]] = PriorityQueue()
pq_updated = asyncio.Event()

async def pull_tasks():
    while True:
        tasks = await find_many()
        for task in tasks:
            await pq.put((task.date, task))
        pq_updated.set()
        await asyncio.sleep(1)


# TODO(shrewd): implement PQ wrapper to get rid of type cast hack
async def push_tasks(dispatch: TaskCallback):
    while True:
        if pq.empty():
            pq_updated.clear()
            await pq_updated.wait()
            continue
        entry = cast(
            "tuple[datetime, Task]",
            pq._queue[0],  # pyright: ignore[reportAttributeAccessIssue] #noqa: SLF001
        )
        due_date, task = entry
        delay = (due_date - utc_now()).total_seconds()
        if delay > 0:
            pq_updated.clear()
            try:
                await asyncio.wait_for(pq_updated.wait(), timeout=delay)
                continue
            except TimeoutError:
                continue
        _, task = pq.get_nowait()
        await dispatch(task)

async def main(dispatch: TaskCallback):
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(pull_tasks())
        task_group.create_task(push_tasks(dispatch))


# if __name__ == "__main__":
#     asyncio.run(main())
