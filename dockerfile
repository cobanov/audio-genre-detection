# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    git \
    cmake \
    build-essential \
    libyaml-cpp-dev \
    libfftw3-dev \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libsamplerate0-dev \
    libtag1-dev \
    libchromaprint-dev \
    curl


# Install the required Python packages
RUN pip3 install essentia-tensorflow fastapi uvicorn

# Create a working directory
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/cobanov/audio-genre-detection.git

# Change working directory to the audio-genre-detection folder
WORKDIR /app/audio-genre-detection

# Expose the port that the application will run on
EXPOSE 8000

# Define the command to run your FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]