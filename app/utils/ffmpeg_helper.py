import os
import subprocess

FFMPEG_PATH = r"C:\libraries\ffmpeg\ffmpeg-essentials_build\bin\ffmpeg.exe"


def extract_audio(video_path: str, audio_path: str):

    if not os.path.exists(video_path):
        raise Exception(f"Video file not found: {video_path}")

    command = [
        FFMPEG_PATH,
        "-i",
        video_path,
        "-vn",
        "-acodec",
        "mp3",
        audio_path,
        "-y"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("FFmpeg extraction failed")