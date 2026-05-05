from fastapi import APIRouter, Form, HTTPException
from utils.auth_utils import hash_password, verify_password
router = APIRouter(tags=["Authentication"])

# Fake "base de données"
fake_users_db = {}


@router.post("/login")
def login_a_user(
    username: str = Form(...),
    password: str = Form(...)
):
    user = fake_users_db.get(username)

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"access_token": username, "token_type": "bearer"}


@router.post("/registration")
def registrate_a_user(
    username: str = Form(...),
    password: str = Form(...)
):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)

    fake_users_db[username] = {
        "password": hashed_password
    }

    return {"message": "User created successfully"}