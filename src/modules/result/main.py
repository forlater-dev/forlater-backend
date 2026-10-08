from typing import TYPE_CHECKING

from contracts.result.main import ResultService as ResultServiceProtocol

if TYPE_CHECKING:
    from contracts.executor.result import ExecutionResult


class ResultService(ResultServiceProtocol):

    async def submit(self, result: ExecutionResult) -> None:
        raise NotImplementedError
