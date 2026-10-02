import asyncio
from abc import ABC, abstractmethod

from db._typing import Task


class Channel(ABC):

    @abstractmethod
    async def push(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    async def pull(self) -> Task:
        raise NotImplementedError

class InMemoryChannel(Channel):

    def __init__(self) -> None:
        self.queue: asyncio.Queue[Task] = asyncio.Queue[Task]()

    async def push(self, task: Task) -> None:
        await self.queue.put(task)

    async def pull(self) -> Task:
        return await self.queue.get()
