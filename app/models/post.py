from pydantic import BaseModel


class Post(BaseModel):
    id: int | None = None
    content: str
    user_id: int





