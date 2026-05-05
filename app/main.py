from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from .routers import auth,post

app = FastAPI(
    title="TruitR",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
