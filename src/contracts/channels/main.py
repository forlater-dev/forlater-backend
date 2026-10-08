from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from contracts.task._typing import Task


class Publisher(Protocol):
    async def push(self, task: Task) -> None: ...


class Consumer(Protocol):
    async def pull(self) -> Task: ...


class Channel(Publisher, Consumer, Protocol):
    pass
