# Audio Genre Detection

The Audio Genre Detection project is a robust and sophisticated system for determining the genre of audio files. Leveraging the power of [Essentia](https://essentia.upf.edu/), a comprehensive library for audio analysis, and TensorFlow, this system provides accurate and efficient genre classification.

It includes a Dockerized environment that streamlines the process of running the audio genre detection system, making it accessible and hassle-free.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker: You need to have Docker installed on your system.

## Getting Started

1. Clone this repository to your local machine.

```bash
git clone https://github.com/cobanov/audio-genre-detection.git
cd audio-genre-detection
```

2. Build and run the docker image

```bash
docker build -t audio-genre-detection .
docker run -it -p 8000:8000 audio-genre-detection
```

## Usage

Once you have set up the environment, you can easily use the audio genre detection system.

Access the SwaggerAPI interface to upload an audio file for genre detection:

```
http://localhost:8000/docs#/
```

The system will process your audio file and provide genre predictions, making it a seamless and efficient solution for genre classification.

## Contributing

We welcome contributions from the community. If you'd like to improve this project or report issues, please refer to our Contribution Guidelines for more information.

## License

This project is licensed under the MIT License, which means it is open-source and free to use, modify, and distribute. Please read the license for more details.
