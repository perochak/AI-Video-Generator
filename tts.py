from TTS.api import TTS

tts_model = TTS(model_name="suhaibrashid17/XTTS-v2-Urdu-FT", progress_bar=False, gpu=True)

def generate_voice(text, output_path):
    tts_model.tts_to_file(text=text, file_path=output_path, speaker_wav=None, language="ur")

