from abc import abstractmethod
from typing import Protocol


class ExecutionResult(Protocol):

    @abstractmethod
    async def success(self): ...

