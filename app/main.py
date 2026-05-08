from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.video_routes import router as video_router

app = FastAPI(title="Video Translator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files

app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# Routes

app.include_router(video_router)