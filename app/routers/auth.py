from fastapi import APIRouter, Form, HTTPException
from utils.auth_utils import hash_password, verify_password
from database.database import get_connection


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login_a_user(
    username: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE pseudo = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(password, user["mot_de_passe"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"access_token": username, "token_type": "bearer"}


@router.post("/registration")
def registrate_a_user(
    username: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE pseudo = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    cursor.execute(
        "INSERT INTO user (pseudo, mot_de_passe) VALUES (?, ?)",
        (username, hashed_password)
    )
    conn.commit()
    conn.close()

    return {"message": "User created successfully"}