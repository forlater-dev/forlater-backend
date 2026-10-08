from collections.abc import Awaitable, Callable

from contracts.executor.result import ExecutionResult

type Submit = Callable[[ExecutionResult], Awaitable[None]]
