from collections.abc import Awaitable, Callable
from db._typing import Task

type Dispatch = Callable[[Task], Awaitable[None]]
type Receive = Callable[[], Awaitable[Task]]
type ExecuteTask = Callable[[Task], Awaitable[None]]
