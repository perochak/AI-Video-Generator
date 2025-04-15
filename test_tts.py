from tts import generate_voice

if __name__ == "__main__":
    urdu_text = "یہ ایک مثال ہے۔"
    output_path = "test_output.wav"
    generate_voice(urdu_text, output_path)
    print(f"Generated voice saved to: {output_path}")
