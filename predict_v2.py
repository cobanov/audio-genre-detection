from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import numpy as np
from essentia.standard import (
    MonoLoader,
    TensorflowPredictEffnetDiscogs,
    TensorflowPredict2D,
)
import os
import subprocess
import requests
from io import BytesIO
import shutil

from labels import labels

app = FastAPI()


class PredictionRequest(BaseModel):
    audio_file: UploadFile = None
    audio_url: str = None


class Predictor:
    def __init__(self):
        self.embedding_model_file = "./models/discogs-effnet-bs64-1.pb"
        self.classification_model_file = "./models/genre_discogs400-discogs-effnet-1.pb"
        self.output = "activations"
        self.sample_rate = 16000

        # Check if model files exist, and download if not
        if not self.check_model_files_exist():
            self.download_models()

        self.loader = MonoLoader()
        self.tensorflowPredictEffnetDiscogs = TensorflowPredictEffnetDiscogs(
            graphFilename=self.embedding_model_file,
            output="PartitionedCall:1",
            patchHopSize=128,
        )
        self.classification_model = TensorflowPredict2D(
            graphFilename=self.classification_model_file,
            input="serving_default_model_Placeholder",
            output="PartitionedCall:0",
        )

    def check_model_files_exist(self):
        return os.path.exists(self.embedding_model_file) and os.path.exists(
            self.classification_model_file
        )

    def download_models(self):
        # Run the download.sh script to fetch the model files
        subprocess.run(["sh", "download.sh"])

    def load_audio_from_file(self, file):
        audio_path = "temp_audio.wav"
        with open(audio_path, "wb") as audio_file:
            shutil.copyfileobj(file, audio_file)
        return audio_path

    def load_audio_from_url(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch audio from the provided URL.")
        audio_data = BytesIO(response.content)
        audio_path = "temp_audio.wav"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data.read())
        return audio_path

    def predict(self, audio_path):
        if not self.check_model_files_exist():
            raise FileNotFoundError(
                "Model files do not exist. Please download them using download.sh script."
            )

        print("Loading audio...")
        self.loader.configure(
            sampleRate=self.sample_rate,
            resampleQuality=4,
            filename=audio_path,
        )
        waveform = self.loader()

        # Model Inferencing
        print("Running the model...")
        embeddings = self.tensorflowPredictEffnetDiscogs(waveform)
        activations = self.classification_model(embeddings)
        activations_mean = np.mean(activations, axis=0)

        # Parsing Genres
        result_dict = dict(zip(labels, activations_mean.tolist()))
        sorted_genres = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
        top_genre = sorted_genres[0][0]
        genre_primary, genre_full = map(str.strip, top_genre.split("---"))
        genre_secondary_full = sorted_genres[1][0]
        genre_secondary = genre_secondary_full.split("---")[1].strip()

        return genre_primary, genre_full, genre_secondary


predictor = Predictor()


@app.post("/predict/")
async def predict_genre(request: PredictionRequest):
    if request.audio_file:
        audio_path = predictor.load_audio_from_file(request.audio_file.file)
    elif request.audio_url:
        audio_path = predictor.load_audio_from_url(request.audio_url)
    else:
        raise ValueError(
            "You must provide either an audio file or an audio URL for prediction."
        )

    try:
        genre_primary, genre_full, genre_secondary = predictor.predict(audio_path)
    finally:
        # Clean up temporary audio file
        os.remove(audio_path)

    return {
        "Primary Genre": genre_primary,
        "Full Genre": genre_full,
        "Secondary Genre": genre_secondary,
    }
