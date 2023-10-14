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

2. Build the docker image

```bash
docker build -t audio-genre-detection .
```

3. Running the Docker Container

You can run the Docker container as follows:

```bash
docker run -it audio-genre-detection
```

4. Inside the Docker container, execute the following command to download the model files using the download.sh script:

```bash
sh ./download.sh
```

To perform audio genre detection using the downloaded models, you can run the inference.py script:

```bash
python inference.py
```

This script will use the downloaded models to make predictions on audio files.
