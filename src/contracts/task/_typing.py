from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


type Pull = Callable[[], Awaitable[list[Task]]]

@dataclass
class Task:
    id: int
    url: int
    date: datetime
