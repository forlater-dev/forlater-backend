from typing import TYPE_CHECKING

from contracts.worker.main import Worker as WorkerProtocol

if TYPE_CHECKING:
    from contracts.channels._typing import Pull
    from contracts.executor._typing import Execute
    from contracts.result._typing import Submit

class Worker(WorkerProtocol):
    async def run(
        self, consume: Pull, execute: Execute, submit: Submit
    ) -> None:
        while True:
            task = await consume()
            result = await execute(task)
            await submit(result)
