from collections.abc import Awaitable, Callable

from db._typing import Task

type TaskCallback = Callable[[Task], Awaitable[None]]
type TaskSource = Callable[[], Awaitable[Task]]
