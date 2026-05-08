from fastapi import APIRouter, UploadFile, File
from app.services.video_service import save_video_and_extract_audio

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

@router.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    result = await save_video_and_extract_audio(video)

    return {
        "message": "Video uploaded successfully",
        "data": result
    }