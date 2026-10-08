from typing import TYPE_CHECKING

from contracts.executor.main import Executor as ExecutorProtocol

if TYPE_CHECKING:
    from contracts.executor.result import ExecutionResult
    from contracts.task._typing import Task


class HttpExecutor(ExecutorProtocol):

    async def execute(self, task: Task) -> ExecutionResult:
        raise NotImplementedError
