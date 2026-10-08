from collections.abc import Awaitable, Callable

from contracts.executor.result import ExecutionResult
from contracts.task._typing import Task

type AsyncCallback[T, R] = Callable[[T], Awaitable[R]]


type TaskSource = Callable[[], Awaitable[Task]]
type TaskExecutor = AsyncCallback[Task, ExecutionResult]
type ResultCallback = AsyncCallback[ExecutionResult, None]
