from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import torch
from diffusers import StableDiffusionPipeline
from gtts import gTTS
import moviepy.editor as mp

# Initialize FastAPI app
app = FastAPI()

# Load AI models
image_model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda")

class SceneRequest(BaseModel):
    story_id: str
    scene_id: int
    text: str  # Scene text
    image_prompt: str  # Image description

@app.post("/process_scene/")
def process_scene(request: SceneRequest):
    try:
        output_dir = f"output/{request.story_id}"
        os.makedirs(output_dir, exist_ok=True)

        # 🎨 Generate Image
        image = image_model(request.image_prompt).images[0]
        image_path = f"{output_dir}/scene_{request.scene_id}.png"
        image.save(image_path)

        # 🔊 Generate Voiceover
        tts = gTTS(text=request.text, lang="en")
        voice_path = f"{output_dir}/scene_{request.scene_id}.mp3"
        tts.save(voice_path)

        # 🎬 Merge Image + Voice to create a scene video
        scene_video_path = f"{output_dir}/scene_{request.scene_id}.mp4"
        create_scene_video(image_path, voice_path, scene_video_path)

        return {"status": "success", "scene_video_url": scene_video_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_scene_video(image_path, audio_path, output_path):
    """
    Creates a video from an image and voiceover.
    """
    image_clip = mp.ImageClip(image_path).set_duration(mp.AudioFileClip(audio_path).duration)
    audio_clip = mp.AudioFileClip(audio_path)
    final_clip = image_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, fps=24, codec="libx264")
