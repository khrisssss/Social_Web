from fastapi import APIRouter, UploadFile, File, HTTPException
from database.database import get_connection
import os

router = APIRouter(tags=["Upload"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_image(user_id: int, image: UploadFile = File(...)):
    if not image.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier fourni")

    path = os.path.join(UPLOAD_FOLDER, image.filename)
    with open(path, "wb") as f:
        f.write(await image.read())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    cursor.execute("UPDATE user SET profil_photo = ? WHERE id = ?", (image.filename, user_id))
    conn.commit()
    conn.close()

    return {"message": "Upload réussi", "path": path}
