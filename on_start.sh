#!/bin/bash

# Navigate to the /app directory (if needed)
cd /app  # The Dockerfile sets the working directory to /app

# Start the FastAPI application using Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 &
