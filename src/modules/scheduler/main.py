import asyncio
from asyncio import Event, PriorityQueue
from typing import TYPE_CHECKING, cast

from contracts.scheduler.main import Scheduler as SchedulerProtocol
from shared.clock import utc_now

if TYPE_CHECKING:
    from datetime import datetime

    from contracts.channels._typing import Push
    from contracts.task._typing import Pull, Task


class Scheduler(SchedulerProtocol):
    def __init__(self) -> None:
        self.pq: PriorityQueue[tuple[datetime, Task]] = PriorityQueue()
        self.pq_updated = Event()

    async def pull_tasks(self, fetch: Pull) -> None:
        while True:
            tasks = await fetch()
            for task in tasks:
                await self.pq.put((task.date, task))
            self.pq_updated.set()
            await asyncio.sleep(1)

    async def push_tasks(self, dispatch: Push) -> None:
        while True:
            if self.pq.empty():
                self.pq_updated.clear()
                await self.pq_updated.wait()
                continue
            entry = cast(
                "tuple[datetime, Task]",
                self.pq._queue[0],  # pyright: ignore[reportAttributeAccessIssue] #noqa: SLF001
            )
            due_date, task = entry
            delay = (due_date - utc_now()).total_seconds()
            if delay > 0:
                self.pq_updated.clear()
                try:
                    await asyncio.wait_for(self.pq_updated.wait(), timeout=delay)
                    continue
                except TimeoutError:
                    continue
            _, task = self.pq.get_nowait()
            await dispatch(task)
