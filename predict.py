import numpy as np
from essentia.standard import (
    MonoLoader,
    TensorflowPredictEffnetDiscogs,
    TensorflowPredict2D,
)

from labels import labels


def process_labels(label):
    genre, style = label.split("---")
    return f"{style}\n({genre})"


processed_labels = list(map(process_labels, labels))


class Predictor:
    def __init__(self):
        """Load the model into memory and create the Essentia network for predictions"""

        self.embedding_model_file = "/models/discogs-effnet-bs64-1.pb"
        self.classification_model_file = "/models/genre_discogs400-discogs-effnet-1.pb"
        self.output = "activations"
        self.sample_rate = 16000

        self.loader = MonoLoader()
        self.tensorflowPredictEffnetDiscogs = TensorflowPredictEffnetDiscogs(
            graphFilename=self.embedding_model_file,
            output="PartitionedCall:1",
            patchHopSize=128,  # remove overlap between patches for efficiency
        )
        self.classification_model = TensorflowPredict2D(
            graphFilename=self.classification_model_file,
            input="serving_default_model_Placeholder",
            output="PartitionedCall:0",
        )

    def predict(self, audio=None):
        """Run a single prediction on the model"""

        print("loading audio...")
        self.loader.configure(
            sampleRate=self.sample_rate,
            resampleQuality=4,
            filename=str(audio),
        )
        waveform = self.loader()

        # Model Inferencing
        print("running the model...")
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
