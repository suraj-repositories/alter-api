import os
import uuid
import pysrt

from faster_whisper import WhisperModel
from fastapi import UploadFile, Request

from app.utils.ffmpeg_helper import extract_audio

UPLOAD_DIR = "storage/uploads"
AUDIO_DIR = "storage/audio"
SUBTITLE_DIR = "storage/subtitles"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(SUBTITLE_DIR, exist_ok=True)

model = WhisperModel("base", device="cpu")


async def save_video_and_extract_audio(request: Request, video: UploadFile):

    video_id = str(uuid.uuid4())

    video_filename = f"{video_id}.mp4"
    audio_filename = f"{video_id}.mp3"
    subtitle_filename = f"{video_id}.srt"

    video_path = os.path.join(UPLOAD_DIR, video_filename)
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    subtitle_path = os.path.join(SUBTITLE_DIR, subtitle_filename)

    # Save video
    with open(video_path, "wb") as buffer:
        buffer.write(await video.read())

    # Extract audio
    extract_audio(video_path, audio_path)

    # Transcribe
    segments, info = model.transcribe(audio_path)

    subtitles = pysrt.SubRipFile()
    transcript = ""

    for index, segment in enumerate(segments, start=1):

        transcript += segment.text + " "

        subtitles.append(
            pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=segment.start),
                end=pysrt.SubRipTime(seconds=segment.end),
                text=segment.text.strip()
            )
        )

    subtitles.save(subtitle_path, encoding="utf-8")

    video_url = request.url_for(
        "storage",
        path=f"uploads/{video_filename}"
    )

    audio_url = request.url_for(
        "storage",
        path=f"audio/{audio_filename}"
    )

    subtitle_url = request.url_for(
        "storage",
        path=f"subtitles/{subtitle_filename}"
    )

    return {
        "video_url": str(video_url),
        "audio_url": str(audio_url),
        "subtitle_url": str(subtitle_url),
        "transcript": transcript.strip(),
        "language": info.language
    }