from fastapi import FastApi 
from pydantic import BaseModel

router = APIRouter(prefix="/post", tags=["Posts"])

class CreateUser(BaseModel):
    id: int 
    username: str
    password: str

class CreateMessage(BaseModel):
    id: int
    user_id: int
    content:str

@post.post("/",)
def home():
    return OK

@post.post("/register")
def register_user (user: CreateUser):
    password = get_password

    conn = get_connection()
    cursor = conn.cursor()

