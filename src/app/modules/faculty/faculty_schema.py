from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.core.schemas import PersistentDeletion, TimestampSchema

class FacultyBase(BaseModel):
    faculty_name: str = Field(..., min_length=2, max_length=250, example="Faculty of Science")

class FacultyCreate(FacultyBase):
    model_config = ConfigDict(extra="forbid")

class FacultyCreateInternal(FacultyCreate):
    pass

class FacultyRead(FacultyBase):
    id: int
    level_id: int
    created_at: datetime

class FacultyUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    faculty_name: Optional[str] = Field(None, min_length=2, max_length=250, example="Faculty of Science")

class FacultyUpdateInternal(FacultyUpdate):
    pass

class FacultyDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool = Field(True, example=True)
    deleted_at: datetime = Field(datetime.now(), example=datetime.now())