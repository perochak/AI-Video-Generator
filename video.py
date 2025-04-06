import moviepy.editor as mpy

def create_video_with_audio(image_path, audio_path, output_path):
    clip = mpy.ImageClip(image_path).set_duration(mpy.AudioFileClip(audio_path).duration)
    clip = clip.set_audio(mpy.AudioFileClip(audio_path))
    clip.write_videofile(output_path, fps=24)

