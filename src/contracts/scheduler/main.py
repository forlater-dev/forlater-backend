from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from contracts.channels._typing import Push
    from contracts.task._typing import Pull

class Scheduler(Protocol):
    async def pull_tasks(self, fetch: Pull) -> None: ...

    async def push_tasks(self, dispatch: Push) -> None: ...
