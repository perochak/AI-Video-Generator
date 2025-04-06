from TTS.api import TTS
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS.from_pretrained("tts_models/multilingual/multi-dataset/xtts_v2", 
                          speaker_wav=None, 
                          language="ur", 
                          use_deepspeed=False)

tts.load_custom_model("suhaibrashid17/XTTS-v2-Urdu-FT")  # <- This is the fine-tuned Urdu model

tts.to(device)

def generate_voice(text, output_path):
    tts.tts_to_file(text=text, file_path=output_path, language="ur")
