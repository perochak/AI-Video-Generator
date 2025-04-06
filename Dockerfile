FROM python:3.10

WORKDIR /app

COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg libgl1 git

# Install Python dependencies
RUN pip install --upgrade pip

# Install PyTorch (adjust CUDA version if needed)
RUN pip install torch==2.2.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Now install other dependencies
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
