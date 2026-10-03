from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db._typing import Task
    from execution_results.main import ExecutionResult, HttpResult


class Executor(ABC):

    @abstractmethod
    async def execute(self, task: Task) -> ExecutionResult:
        raise NotImplementedError


class HttpExecutor(Executor):

    def __init__(self) -> None:
        pass

    async def execute(self, task: Task) -> HttpResult:
        raise NotImplementedError

