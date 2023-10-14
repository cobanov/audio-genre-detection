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
    libavresample-dev \
    libsamplerate0-dev \
    libtag1-dev \
    libchromaprint-dev \
    curl

# Clone the Essentia repository from GitHub
RUN git clone https://github.com/MTG/essentia.git

# Build and install Essentia
RUN cd essentia && \
    mkdir build && cd build && \
    cmake .. && \
    make && \
    make install

# Install the required Python packages
RUN pip3 install essentia-tensorflow

# Start a bash shell as the entry point
CMD ["/bin/bash"]
