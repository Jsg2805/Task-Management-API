# dto/schemas.py
from datetime import datetime
from enum import Enum
from typing import Optional


# Enums
class PriorityEnum(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class StatusEnum(str, Enum):
    TODO = 'TO DO'
    IN_PROGRESS = 'IN PROGRESS'
    DONE = 'DONE'


# Simple data containers (used for internal reference)
class User:
    def __init__(self, user_id: int, uname: str, uemail: str):
        self.user_id = user_id
        self.uname = uname
        self.uemail = uemail


class Task:
    def __init__(
        self,
        task_id: int,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[PriorityEnum] = None,
        status: Optional[StatusEnum] = StatusEnum.TODO,
        user_id: Optional[int] = None
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.user_id = user_id
