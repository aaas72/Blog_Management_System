from pydantic import BaseModel, constr, ConfigDict
from typing import Optional
from datetime import datetime
from models.post_model import PostStatus

class PostCreate(BaseModel):
    title: constr(min_length=3)
    content: constr(min_length=10)

class PostUpdate(BaseModel):
    title: Optional[constr(min_length=3)] = None
    content: Optional[constr(min_length=10)] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    status: PostStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
