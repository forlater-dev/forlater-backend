from typing import TYPE_CHECKING

from contracts.task.main import TaskService as TaskServiceProtocol

if TYPE_CHECKING:
    from contracts.task._typing import Task


class TaskService(TaskServiceProtocol):
    async def find_due(self) -> list[Task]:
        raise NotImplementedError
