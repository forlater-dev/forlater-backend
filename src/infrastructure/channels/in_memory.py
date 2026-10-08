import asyncio

from src.contracts.channels.main import Channel
from src.contracts.task._typing import Task


class InMemoryChannel(Channel):
    def __init__(self) -> None:
        self.queue: asyncio.Queue[Task] = asyncio.Queue[Task]()

    async def push(self, task: Task) -> None:
        return await self.queue.put(task)

    async def pull(self) -> Task:
        return await self.queue.get()
