import asyncio

import scheduler
import worker

from db._typing import Task
from executors.main import HttpExecutor

ready: asyncio.Queue[Task] = asyncio.Queue[Task]()

async def main():

    executor = HttpExecutor()

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(scheduler.main(ready.put))
        task_group.create_task(worker.main(ready.get, executor.execute))


if __name__ == "__main__":
    asyncio.run(main())
