import uuid

from pydantic import BaseModel
from pydantic import ConfigDict

class CommentBase(BaseModel):
    id: str = uuid.uuid4().hex
    task_id: str
    content: str
