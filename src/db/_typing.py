from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

@dataclass
class Task:
    id: int
    url: int
    date: datetime
