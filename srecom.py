# Temp 3

import os
import time
import json
import librosa
import argparse
import subprocess
import numpy as np
import tensorflow as tf

from scipy.spatial.distance import cosine, euclidean
from createPlaylist import populate_playlist
from sklearn.decomposition import PCA


start_time = time.time()

def extract_audio_features(file_path, sr=16000, n_mfcc=14, n_fft=1048, hop_length=512):
    try:
        y, sr = librosa.load(file_path, sr=sr)
        # y_tensor = tf.convert_to_tensor(y, dtype=tf.float32)

        # MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
        mfcc_mean = np.mean(mfccs, axis=1)

        # Spectral Features
        rms = librosa.feature.rms(y=y).flatten()
        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length).flatten()
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length).flatten()

        # Tonnetz
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        tonnetz_mean = np.mean(tonnetz, axis=1)

        # Chroma Features
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)
        chroma_mean = np.mean(chroma, axis=1)

        # Feature Weighting
        features = np.concatenate([
        mfcc_mean.astype(np.float32) * 1.5,                     # represents timbre and tone color     
        [np.mean(rms).astype(np.float32) * 0.5],                # represents the energy/loudness of the audio
        [np.mean(spec_centroid).astype(np.float32) * 0.5],      # represents the "brightness" of the sound
        [np.mean(rolloff).astype(np.float32) * 0.5],            # represents the frequency where most energy is concentrated
        tonnetz_mean.astype(np.float32) * 1.2,                  # represents harmonic content and musical key
        chroma_mean.astype(np.float32) * 1.3                    # represents pitch class distribution, emphasizing harmonic characteristics
        ], dtype=np.float32)

        return features
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None
    


def process_directory(directory_path, feature_file="features.json"):
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(('.mp3', '.wav', '.flac'))]
    
    features = {}
    for file_path in file_paths:
        feature_vector = extract_audio_features(file_path)
        if feature_vector is not None:
            features[os.path.basename(file_path)] = feature_vector.tolist()

    with open(feature_file, "w") as f:
        json.dump(features, f)

    return list(features.keys())



def recommend_songs(song_name, feature_file="features.json", top_n=5, epsilon=1e-5):
    with open(feature_file, "r") as f:
        features = json.load(f)

    song_names = list(features.keys())

    if song_name not in features:
        print(f"Song '{song_name}' not found in processed features.")
        return []

    target_features = np.array(features[song_name])

    similarities = []
    for other_song, other_features in features.items():
        if other_song != song_name:
            other_features = np.array(other_features)
            cos_sim = 1 - cosine(target_features, other_features)
            eucl_dist = euclidean(target_features, other_features)
            hybrid_score = cos_sim / (eucl_dist + epsilon)
            similarities.append((other_song, hybrid_score))

    sorted_songs = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [song for song, _ in sorted_songs[:top_n]]


def reduce_features(features, n_components=10):
    pca = PCA(n_components=n_components)
    reduced_features = pca.fit_transform(features)
    return reduced_features


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("link", type=str, help="The link to the playlist URL")
    args = parser.parse_args()
    link = args.link

    getTopTracksVbScript = "downloadTopTracks.vbs"
    getDailyTracksVbScript = "downloadDailyPlaylist.vbs"
    moveTopToDailyVbScript = "moveTopToDaily.vbs"
    emptyDirectories = "emptyDirectories.vbs"

    subprocess.run(['cscript', getDailyTracksVbScript, link], check=True)
    subprocess.run(['cscript', moveTopToDailyVbScript], check=True)
    
    directory_path = "DailyTracks\\daily"
    print(f"Processing songs in directory: {directory_path}\n")

    recommendations_list = []
    try:
        process_directory(directory_path)
        with open("top_track_names.txt", 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()

        for line in lines:
            target_song = line + '.mp3'
            recommendations = recommend_songs(target_song)
            print(recommendations)
            recommendations_list += recommendations

            print(f"\nRecommendations for '{target_song}':")
            for rec in recommendations:
                print(f"  {rec}")

        recommendations_list = list(set(recommendations_list))
        recommendations_list = [song[:-4] for song in recommendations_list]

        populate_playlist(recommendations_list)

        # Delete downloaded songs to free space after run
        subprocess.run(['cscript', emptyDirectories], check=True)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Runtime: {elapsed_time} seconds")


    except Exception as e:
        print(f"Error: {e}")
