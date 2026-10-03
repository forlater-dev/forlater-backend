from abc import ABC, abstractmethod


class ExecutionResult(ABC):

    @abstractmethod
    async def success(self):
        raise NotImplementedError

class HttpResult(ExecutionResult):

    async def success(self):
        raise NotImplementedError
