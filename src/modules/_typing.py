from collections.abc import Awaitable, Callable

from db._typing import Task
from execution_results.main import ExecutionResult

type AsyncCallback[T, R] = Callable[[T], Awaitable[R]]


type TaskSource = Callable[[], Awaitable[Task]]
type TaskExecutor = AsyncCallback[Task, ExecutionResult]
type ResultCallback = AsyncCallback[ExecutionResult, None]

