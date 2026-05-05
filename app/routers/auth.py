from fastapi import APIRouter, Form

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login_a_user(
    username: str = Form(...),
    password: str = Form(...)
):
    
    return {"access_token": username, "token_type": "bearer"}

@router.post("/registration")
def registrate_a_user()
    