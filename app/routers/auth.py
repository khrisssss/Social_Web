from fastapi import APIRouter, Form
from app.models.user import RegistrationUser

app = APIRouter(tite="Registration")


# welcome 
@app.get("/")
def welcome():
    return {"message":"Welcome to your Registeration!"}


@app.post("/register")
def registration(user: RegistrationUser):
    success = user.userID, user.username, user.password
    password: str
    