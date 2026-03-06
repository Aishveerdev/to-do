from sqlmodel import SQLModel , Field
from pydantic import ConfigDict
from typing import Optional


# All these schemas would be gaurds stadning outside the endpoints to validate data.

class taskCreate(SQLModel):
    title: str = Field(nullable=False)
    description: str


class taskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class taskResponse(SQLModel):
    id: int
    title: str
    description: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)
    