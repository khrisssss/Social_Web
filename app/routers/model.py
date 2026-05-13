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

#HF_TOKEN = os.getenv("HF_TOKEN")
router = APIRouter(tags=["model"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/generer_image")
async def generer_image(prompt: Prompt, current_user: dict = Depends(get_current_user)):
    print("current_user =", current_user)
    encoded_prompt = quote(prompt.prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    print(url)
    response = requests.post(url)
    print(response.status_code)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)
    image_bytes = response.content
    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(UPLOAD_FOLDER, filename)

    with open(path, "wb") as f:
        f.write(image_bytes)
    user_id = str(current_user["id"])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    cursor.execute("UPDATE user SET profil_photo = ? WHERE id = ?", (filename, user_id))
    conn.commit()
    conn.close()

    return FileResponse(path, media_type="image/png", filename=filename)


