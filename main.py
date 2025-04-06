from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
import subprocess
import shutil
import time
import threading
import ftplib

# Import your actual modules for image, tts, video etc.
from tts import generate_voice
from diffusion import generate_image
from video import create_video_with_audio

app = FastAPI()

# Track status of each scene
scene_status = {}  # {0: "pending" | "processing" | "done" | "error"}
scene_outputs = {}  # {0: "path/to/scene0.mp4"}

# === Input model ===
class Character(BaseModel):
    name: Optional[str] = None
    mood: Optional[str] = None

class Scene(BaseModel):
    scene_title: Optional[str] = ""
    setting: Optional[str] = ""
    characters: List[Character] = []
    voice_over: str
    tone: Optional[str] = ""
    image_prompt: str

# === Background worker ===
def process_scene(scene: Scene, index: int):
    try:
        scene_status[index] = "processing"
        output_dir = f"scenes/scene_{index}"
        os.makedirs(output_dir, exist_ok=True)

        # Image generation
        image_path = os.path.join(output_dir, "image.png")
        generate_image(scene.image_prompt, image_path)

        # TTS
        audio_path = os.path.join(output_dir, "audio.wav")
        generate_voice(scene.voice_over, audio_path)

        # Video
        video_path = os.path.join(output_dir, "video.mp4")
        create_video_with_audio(image_path, audio_path, video_path)

        scene_outputs[index] = video_path
        scene_status[index] = "done"
    except Exception as e:
        print(f"Error in scene {index}: {e}")
        scene_status[index] = "error"

@app.post("/process_scene")
def receive_scene(scene: Scene, scene_index: int):
    scene_status[scene_index] = "pending"
    threading.Thread(target=process_scene, args=(scene, scene_index)).start()
    return {"status": "processing", "scene_index": scene_index}

@app.get("/status")
def get_status(scene_index: Optional[int] = None):
    if scene_index is not None:
        return {
            "scene_index": scene_index,
            "status": scene_status.get(scene_index, "unknown")
        }
    return {"scenes": scene_status}

@app.get("/finalize_video")
def finalize_and_upload():
    final_path = "final_video.mp4"
    with open("filelist.txt", "w") as f:
        for i in sorted(scene_outputs.keys()):
            f.write(f"file '{scene_outputs[i]}'\n")
    # Merge with ffmpeg
    subprocess.call([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", "filelist.txt",
        "-c", "copy", final_path
    ])
    upload_to_ftp(final_path)
    return {"status": "done", "path": final_path}

def upload_to_ftp(file_path):
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
    with open(file_path, 'rb') as f:
        session.storbinary(f'STOR {os.path.basename(file_path)}', f)
    session.quit()
