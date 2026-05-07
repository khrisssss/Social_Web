from fastapi import APIRouter, UploadFile, File, HTTPException
import os

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    if not image.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier fourni")

    path = os.path.join(UPLOAD_FOLDER, image.filename)
    with open(path, "wb") as f:
        f.write(await image.read())

    return {"message": "Upload réussi", "path": path}
