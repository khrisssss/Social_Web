from fastapi import APIRouter, Depends, File, HTTPException
import requests
from fastapi.responses import FileResponse
from database.database import get_connection
from pydantic import BaseModel
from utils.auth_utils import get_current_user
import os
from dotenv import load_dotenv
import uuid
from urllib.parse import quote

load_dotenv()

class Prompt(BaseModel):
      prompt: str

router = APIRouter(tags=["model"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/generer_image")
async def generer_image(prompt: Prompt):
    encoded_prompt = quote(prompt.prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    response = requests.post(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)
    image_bytes = response.content
    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "wb") as f:
        f.write(image_bytes)
    return {"filename": filename}

class ImageAttribution(BaseModel):
    filename: str
    
@router.post("/image_user")
async def attribuer_image(data : ImageAttribution, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["id"])
    path = os.path.join(UPLOAD_FOLDER, data.filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image introuvable!")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    cursor.execute("UPDATE user SET profil_photo = ? WHERE id = ?", (filename, user_id))
    conn.commit()
    conn.close()

    return FileResponse(path, media_type="image/png", filename=data.filename)
