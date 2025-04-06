from TTS.api import TTS
import torch

# Use .to(device) instead of gpu=True
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model and move it to the right device
tts_model = TTS(model_name="suhaibrashid17/XTTS-v2-Urdu-FT", progress_bar=False)
tts_model.to(device)

def generate_voice(text, output_path):
    tts_model.tts_to_file(text=text, file_path=output_path, speaker_wav=None, language="ur")
