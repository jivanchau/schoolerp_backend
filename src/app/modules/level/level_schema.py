from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from app.core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class LevelBase(BaseModel):
    level_name: Annotated[str, Field(min_length=2, max_length=30, examples=["This is my level"])]

class LevelRead(BaseModel):
    levelID: int
    level_name: Annotated[str, Field(min_length=2, max_length=30, examples=["This is my level"])]
    created_at: datetime

class LevelCreate(LevelBase):
    model_config = ConfigDict(extra="forbid")

class LevelCreateInternal(LevelCreate):
    pass

class LevelUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level_name: Annotated[str, Field(min_length=2, max_length=30, examples=["This is my level"])]
    
class LevelUpdateInternal(LevelCreate):
    pass

class LevelDelete(BaseModel):
    pass