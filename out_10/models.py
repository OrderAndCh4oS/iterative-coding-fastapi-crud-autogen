# filename: models.py

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Customer:
    uuid: UUID
    email: str
    username: str
    created_at: datetime
    updated_at: datetime
