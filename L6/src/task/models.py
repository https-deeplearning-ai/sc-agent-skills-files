from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    title: str
    done: bool = False
    priority: Priority = Priority.LOW
    created_at: datetime = field(default_factory=datetime.now)
    due_date: datetime | None = None
