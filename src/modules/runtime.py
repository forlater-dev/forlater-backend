import asyncio

import scheduler
import worker

from channels.main import Channel, InMemoryChannel
from executors.main import Executor, HttpExecutor


async def main():
    executor: Executor = HttpExecutor()
    channel: Channel = InMemoryChannel()

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(scheduler.main(channel.push))
        task_group.create_task(worker.main(channel.pull, executor.execute))


if __name__ == "__main__":
    asyncio.run(main())
