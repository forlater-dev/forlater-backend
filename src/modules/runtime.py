import asyncio

import scheduler
import worker

from channels.main import Channel, InMemoryChannel
from db.tasks import find_many
from executors.main import Executor, HttpExecutor
from result_service.main import InMemoryResultService, ResultService


async def main():
    executor: Executor = HttpExecutor()
    channel: Channel = InMemoryChannel()
    result_service: ResultService = InMemoryResultService()

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(scheduler.main(find_many, channel.push))
        task_group.create_task(
            worker.main(channel.pull, executor.execute, result_service.submit_result)
        )


if __name__ == "__main__":
    asyncio.run(main())
