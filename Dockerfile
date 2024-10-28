FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

COPY docker_requirements.txt /app/

RUN pip install --no-cache-dir -r docker_requirements.txt

# Copy the specific script that requires Python 3.12
COPY voice_detector.py /app/
COPY llama.py /app/


# Expose the port the API will listen on
EXPOSE 5000

# Command to run your script
CMD ["python", "voice_detector.py"]