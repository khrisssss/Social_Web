from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from utils.auth_utils import hash_password, verify_password
from database.database import get_connection
import secrets


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

    return {"User connected ": user["pseudo"]}


@router.post("/registration")
def registrate_a_user(userConnect: UserModel):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE pseudo = ?", (userConnect.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")

    hashed_password = hash_password(userConnect.password)
    user_id = secrets.randbelow(10**15)
    cursor.execute(
        "INSERT INTO user (id, pseudo, mot_de_passe) VALUES (?, ?, ?)",
        (user_id, userConnect.username, hashed_password)
    )
    conn.commit()
    conn.close()

    return {"message": "User créé"}