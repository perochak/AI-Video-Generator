from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import moviepy.editor as mp
import os

app = FastAPI()

class MergeRequest(BaseModel):
    story_id: str
    scene_ids: List[int]  # Ordered list of scene IDs
    title: str  # Intro title
    outro_text: str = "Thanks for watching! Subscribe for more."  # Outro text

@app.post("/merge_scenes/")
def merge_scenes(request: MergeRequest):
    try:
        output_dir = f"output/{request.story_id}"
        scene_videos = [f"{output_dir}/scene_{scene_id}.mp4" for scene_id in request.scene_ids]

        # 🎬 Load all scenes
        clips = [mp.VideoFileClip(scene) for scene in scene_videos]

        # 🎬 Create Intro
        intro_clip = generate_intro(request.title, clips[0].size)

        # 🎬 Create Outro
        outro_clip = generate_outro(request.outro_text, clips[0].size)

        # 📌 Add smooth transitions
        final_clips = [intro_clip]
        for i, clip in enumerate(clips):
            if i > 0:
                transition = mp.ColorClip(size=clip.size, color=(0, 0, 0), duration=0.5)
                final_clips.append(transition)
            final_clips.append(clip)
        final_clips.append(outro_clip)

        # 🎬 Merge everything into the final movie
        final_video = mp.concatenate_videoclips(final_clips, method="compose")
        final_video_path = f"{output_dir}/final_movie.mp4"
        final_video.write_videofile(final_video_path, fps=24, codec="libx264")

        return {"status": "success", "final_movie_url": final_video_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_intro(title, size):
    """
    Generates an engaging intro with animated text.
    """
    duration = 3
    bg_color = (30, 30, 30)

    text_clip = mp.TextClip(title, fontsize=70, color='white', font="Arial-Bold")\
                 .set_position('center')\
                 .set_duration(duration)\
                 .fadein(1).fadeout(1)

    bg_clip = mp.ColorClip(size=size, color=bg_color, duration=duration)
    return mp.CompositeVideoClip([bg_clip, text_clip])

def generate_outro(text, size):
    """
    Creates an outro with a call to action.
    """
    duration = 3
    bg_color = (0, 0, 0)

    text_clip = mp.TextClip(text, fontsize=50, color='yellow', font="Arial-Bold")\
                 .set_position('center')\
                 .set_duration(duration)\
                 .fadein(1).fadeout(1)

    bg_clip = mp.ColorClip(size=size, color=bg_color, duration=duration)
    return mp.CompositeVideoClip([bg_clip, text_clip])
