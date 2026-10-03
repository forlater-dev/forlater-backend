import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typing import ResultCallback, TaskExecutor, TaskSource


async def run(
    receive: TaskSource,
    execute: TaskExecutor,
    dispatch_result: ResultCallback,
):
    while True:
        task = await receive()
        result = await execute(task)
        await dispatch_result(result)


async def main(
    receive: TaskSource,
    execute: TaskExecutor,
    dispatch_result: ResultCallback,
):
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(run(receive, execute, dispatch_result))


# if __name__ == "__main__":
#     asyncio.run(main())
