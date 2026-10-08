from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.contracts.executor.result import ExecutionResult


class ResultService(Protocol):
    @abstractmethod
    async def submit(self, result: ExecutionResult) -> None:
        raise NotImplementedError
