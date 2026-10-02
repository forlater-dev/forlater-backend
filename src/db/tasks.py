from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typing import Task

# Temporary Mock

async def find_many() -> list[Task]:
    raise NotImplementedError

async def update() -> None:
    raise NotImplementedError

