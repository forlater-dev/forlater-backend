from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from contracts.task._typing import Task


class TaskService(Protocol):
    @abstractmethod
    async def find_due(self) -> list[Task]:
        raise NotImplementedError
