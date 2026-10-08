from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from result import ExecutionResult
    from task._typing import Task


class Executor(Protocol):

    async def execute(self, task: Task) -> ExecutionResult: ...
