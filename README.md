# Song Recommender By Audio Features
Recommend songs based on a song in terms of its audio features of:

* MFCCs
* RMS Energy
* Spectral Centroid
* Spectral Rolloff
* Tonnetz

## Example Usage
Add the path to the directory containing the songs
```python
if __name__ == "__main__":
    path = ""

    try:
        # Process directory and extract features
        raw_features = process_directory(path)

        # Normalize and reduce dimensions
        normalized_features, song_names = normalize_features(raw_features)
        reduced_features = reduce_dimensions(normalized_features, n_components=10)

        anchor_song = song_names[0] 
        recommendations = recommend_songs(anchor_song, reduced_features, song_names)

        print(f"\nRecommendations for '{anchor_song}':")
        for rec in recommendations:
            print(f"  {rec}")
    except Exception as e:
        print(f"Error: {e}")
