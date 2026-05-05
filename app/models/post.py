from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    email: str


class UserIn(User):
    password: str


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    image_url: Optional[str] = None


