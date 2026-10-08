from collections.abc import Awaitable, Callable

from contracts.executor.result import ExecutionResult
from contracts.task._typing import Task

type Execute = Callable[[Task], Awaitable[ExecutionResult]]
