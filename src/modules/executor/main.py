from typing import TYPE_CHECKING

from srcc.contracts.executor.main import Executor as ExecutorProtocol

if TYPE_CHECKING:
    from srcc.contracts.executor.result import ExecutionResult
    from srcc.contracts.tasks._typing import Task


class HttpExecutor(ExecutorProtocol):

    async def execute(self, task: Task) -> ExecutionResult:
        raise NotImplementedError
