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
RUN pip3 install essentia-tensorflow

# Create a working directory
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/cobanov/audio-genre-detection.git

# Change working directory to the audio-genre-detection folder
WORKDIR /app/audio-genre-detection

CMD ["/bin/bash"]