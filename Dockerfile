FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Install system dependencies
RUN apt update && apt install -y \
    python3 python3-pip ffmpeg git curl \
    && apt clean

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install fastapi uvicorn moviepy diffusers transformers gtts pydub

# Clone your AI project repository (or upload your files)
WORKDIR /app
RUN git clone https://github.com/perochak/AI-Video-Generator.git .
# If no GitHub repo, upload manually later

# Set up API server
CMD ["sh", "-c", "uvicorn process_scenes:app --host 0.0.0.0 --port 8000 & uvicorn merge_scenes:app --host 0.0.0.0 --port 8001"]
