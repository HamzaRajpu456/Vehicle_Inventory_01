from sqlmodel import  SQLModel, Field
from uuid import UUID, uuid4
from datetime  import datetime, timezone
from typing import Optional

class BaseModel(SQLModel):

    id : Optional[UUID] = Field(default_factory = uuid4, primary_key = True, index = True)
    created_at : datetime = Field(default_factory = lambda :  datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))

    class Config:
         orm_model = True









