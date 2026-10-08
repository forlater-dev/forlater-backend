from collections.abc import Awaitable, Callable

from contracts.task._typing import Task

type Push = Callable[[Task], Awaitable[None]]
type Pull = Callable[[], Awaitable[Task]]

