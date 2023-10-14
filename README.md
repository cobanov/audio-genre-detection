# Audio Genre Detection

This project is aimed at audio genre detection using [Essentia](https://essentia.upf.edu/), a library for audio analysis, and TensorFlow. It includes a Dockerfile for creating a containerized environment for running the audio genre detection system.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker: You need to have Docker installed on your system.

## Usage

1. Clone this repository to your local machine.

```bash
git clone https://github.com/cobanov/audio-genre-detection.git
cd audio-genre-detection
```

2. Build  and run the docker image

```bash
docker build -t audio-genre-detection .
docker run -it -p 8000:8000 audio-genre-detection
```
