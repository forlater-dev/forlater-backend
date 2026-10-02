import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typing import TaskCallback, TaskSource

async def run(receive: TaskSource, execute: TaskCallback):
    while True:
        task = await receive()
        await execute(task)


async def main(receive: TaskSource, execute: TaskCallback):
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(run(receive, execute))


# if __name__ == "__main__":
#     asyncio.run(main())
