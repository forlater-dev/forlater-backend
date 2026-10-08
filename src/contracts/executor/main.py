from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from contracts.executor.result import ExecutionResult
    from contracts.task._typing import Task


class Executor(Protocol):

    async def execute(self, task: Task) -> ExecutionResult: ...
