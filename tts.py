import torch
from transformers import VitsModel, AutoTokenizer
import scipy.io.wavfile as wav

def generate_voice(text: str, output_path: str):
    # Load the pre-trained model and tokenizer
    model = VitsModel.from_pretrained("facebook/mms-tts-urd-script_devanagari")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-urd-script_devanagari")

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt")

    # Generate the speech waveform
    with torch.no_grad():
        mel_output, _, _ = model(input_ids=inputs["input_ids"])

    # Convert the generated mel spectrogram to waveform (this might depend on the model type)
    waveform = model.decode(mel_output)

    # Save the waveform as a .wav file
    wav.write(output_path, 22050, waveform.squeeze().cpu().numpy())