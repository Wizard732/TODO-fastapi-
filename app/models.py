from pydantic import BaseModel, Field
from typing import Optional

class OldTask(BaseModel):
    id: int = Field(gt=0)
    status: bool = Field(default=True)
    title: str = Field(min_length=2, max_length=10)
    description: str = Field(default=None)
    priority: int = Field(gt=0, le=5)


class NewTask(BaseModel):
    id: Optional[int] = None
    status: bool = Field(default=True)
    title: str = Field(min_length=2, max_length=10)
    description: str = Field(default=None)
    priority: int = Field(gt=0, le=5)
