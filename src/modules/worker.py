import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typing import ExecuteTask, Receive

async def run(receive: Receive, execute: ExecuteTask):
    while True:
        task = await receive()
        await execute(task)


async def main(receive: Receive, execute: ExecuteTask):
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(run(receive, execute))


# if __name__ == "__main__":
#     asyncio.run(main())
