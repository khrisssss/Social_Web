from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from utils.auth_utils import hash_password, verify_password, create_access_token
from database.database import get_connection


router = APIRouter(tags=["Authentication"])

class UserModel(BaseModel):
    username: str
    password: str


@router.post("/login")
def login_a_user(userConnect: UserModel):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE pseudo = ?", (userConnect.username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(userConnect.password, user["mot_de_passe"]):
        raise HTTPException(status_code=400, detail="Identification incorrect")

    token = create_access_token(user["pseudo"], user["id"])
    return {"access_token": token, "token_type": "bearer"}


@router.post("/registration")
def registrate_a_user(userConnect: UserModel):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE pseudo = ?", (userConnect.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")

    hashed_password = hash_password(userConnect.password)
    cursor.execute(
        "INSERT INTO user (pseudo, mot_de_passe) VALUES (?, ?)",
        (userConnect.username, hashed_password)
    )
    conn.commit()
    conn.close()

    return {"message": "User créé"}