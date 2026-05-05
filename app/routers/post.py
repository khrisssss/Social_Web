from fastapi import FastApi 
from pydantic import BaseModel

post = FastApi(prefix="/post")

class CreateUser(BaseModel):
    id: int 
    username: str
    password: str

class CreateMessage(BaseModel):
    id: int
    user_id: int
    content:str

@post.post("/",)
def create_post(post: 
