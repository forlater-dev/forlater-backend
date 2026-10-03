from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from execution_results.main import ExecutionResult


class ResultService(ABC):

    @abstractmethod
    async def submit_result(self, result: ExecutionResult) -> None:
        raise NotImplementedError


class InMemoryResultService(ResultService):

    def __init__(self) -> None:
        pass

    async def submit_result(self, result: ExecutionResult) -> None:
        raise NotImplementedError
