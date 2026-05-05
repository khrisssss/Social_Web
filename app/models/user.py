from pydantic import BaseModel


class CreateUser(BaseModel):
    id: int | None = None
    username: str


class UserIn(User):
    password: str