FROM python:3.10

WORKDIR /app

# Copy the application code and the bash script into the container
COPY . .

# Copy the on_start.sh script to the container
COPY on_start.sh /app/on_start.sh

# Make the bash script executable
RUN chmod +x /app/on_start.sh

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg libgl1 git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod -R 755 /app/

# Expose the port the app will run on
EXPOSE 8000

# Use the bash script to start the app
CMD ["/app/on_start.sh"]
