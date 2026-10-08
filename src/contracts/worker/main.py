from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from contracts.channels._typing import Pull
    from contracts.executor._typing import Execute
    from contracts.result._typing import Submit


class Worker(Protocol):
    async def run(self, consume: Pull, execute: Execute, submit: Submit) -> None: ...
