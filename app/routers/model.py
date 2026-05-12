from fastapi import APIRouter, Depends, File, HTTPException
import requests
from fastapi.responses import FileResponse
from database.database import get_connection
from pydantic import BaseModel
from utils.auth_utils import get_current_user
import os
#from diffusers import FluxPipeline
from dotenv import load_dotenv


load_dotenv()

class Prompt(BaseModel):
      prompt: str

HF_TOKEN = os.getenv("HF_TOKEN")
router = APIRouter(tags=["model"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@router.post("/prompt")
def prompt_demande(prompt : Prompt, current_user: dict = Depends(get_current_user)):
    return {
        "prompt": prompt.prompt,
        "author": current_user["username"]
    }

@router.post("/generer_image")
def generer_image(prompt: Prompt, current_user: dict = Depends(get_current_user)):

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt.prompt}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    image_bytes = response.content

    filename = "flux.png"
    path = os.path.join(UPLOAD_FOLDER, filename)

    with open(path, "wb") as f:
        f.write(image_bytes)

    return FileResponse(path, media_type="image/png", filename=filename)


# router = APIRouter(tags=["model"])

# pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.float32)
# pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power


# class Prompt(BaseModel):
#     prompt: str

# @router.post("/prompt")
# def create_post(prompt : Prompt, current_user: dict = Depends(get_current_user)):
#     return {
#         "prompt": prompt.prompt,
#         "author": current_user["username"]
#     }

# @router.get("/generer_image")
# async def generer_image(prompt : Prompt, current_user: dict = Depends(get_current_user)):
    
#     image = pipe(
#         prompt.prompt,
#         height=256,
#         width=256,
#         guidance_scale=1.5,
#         num_inference_steps=4,
#         max_sequence_length=64,
#         generator=torch.Generator("cpu").manual_seed(0)
#     ).images[0]
#     filename = "flux-dev.png"

#     path = os.path.join(UPLOAD_FOLDER, filename)
#     image.save(path)

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM user WHERE id = ?", (current_user["id"],))
#     if not cursor.fetchone():
#         conn.close()
#         raise HTTPException(status_code=404, detail="Utilisateur introuvable")

#     cursor.execute("UPDATE user SET profil_photo = ? WHERE id = ?", (filename, current_user["id"]))
#     conn.commit()
#     conn.close()

#     return FileResponse(path, media_type="image/png", filename=filename)

