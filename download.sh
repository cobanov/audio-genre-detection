mkdir models
mkdir assets
curl -L -o assets/sample.mp3 "https://diktator-demo.s3.amazonaws.com/selintunr%40gmail.com/original/deneme_0c75dbb0-3754-446b-ab91-c9592ed0bdd3.mp3"
curl -L -o models/discogs-effnet-bs64-1.pb "https://essentia.upf.edu/models/feature-extractors/discogs-effnet/discogs-effnet-bs64-1.pb"
curl -L -o models/genre_discogs400-discogs-effnet-1.pb "https://essentia.upf.edu/models/classification-heads/genre_discogs400/genre_discogs400-discogs-effnet-1.pb"
echo env is ready!"