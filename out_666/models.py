# filename: models.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Customer(BaseModel):
    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    username: str
    createdAt: Optional[datetime] = Field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.now)