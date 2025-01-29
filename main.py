import librosa
import numpy as np
import torch
from torch import tensor
import os
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from umap import UMAP

def extract_audio_features(file_path, sr=22050, n_mfcc=20, n_fft=2048, hop_length=512):
    """
    Parameters:
        file_path (str): Path to the audio file.
        sr (int): Sampling rate for loading audio.
        n_mfcc (int): Number of MFCCs to extract.
        n_fft (int): Number of FFT components.
        hop_length (int): Hop length for FFT.

    Returns:
        features (list): List of extracted features.
    """
    try:
        y, sr = librosa.load(file_path, sr=sr)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        y_tensor = tensor(y, device=device, dtype=torch.float32)

        rms = librosa.feature.rms(y=y).flatten()
        rms_mean = np.mean(rms)

        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length).flatten()
        spec_centroid_mean = np.mean(spec_centroid)

        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length).flatten()
        rolloff_mean = np.mean(rolloff)

        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        tonnetz_mean = np.mean(tonnetz, axis=1)

        try:
            stft_gpu = torch.stft(
                y_tensor, n_fft=n_fft, hop_length=hop_length, return_complex=True
            ).abs()
            stft_cpu = stft_gpu.cpu().numpy()
        except RuntimeError as e:
            print(f"Warning: {e}. Falling back to CPU for FFT.")
            stft_cpu = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

        mfccs = librosa.feature.mfcc(S=librosa.power_to_db(stft_cpu), n_mfcc=n_mfcc)
        mfcc_mean = np.mean(mfccs, axis=1)

        features = np.concatenate(
            [
                mfcc_mean,          
                [rms_mean],         
                [spec_centroid_mean], 
                [rolloff_mean],     
                tonnetz_mean        
            ]
        )
        return features
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def process_directory(path):
    """
    Parameters:
        path (str): Path to the directory containing the audio files.

    Returns:
        all_features (dict): A dictionary with file names as the keys and features as its values.
    """
    file_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.mp3', '.wav', '.flac'))]

    features = {}
    for file_path in file_paths:
        features[os.path.basename(file_path)] = extract_audio_features(file_path)
    return features


def normalize_features(features):
    """
    Parameters:
        features (dict): Dictionary of features.

    Returns:
        normalized_features (np.ndarray): Normalized feature matrix.
        song_names (list): List of song names.
    """
    feature_matrix = []
    song_names = []

    for song_name, feature_vector in features.items():
        feature_matrix.append(feature_vector)
        song_names.append(song_name)

    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(feature_matrix)
    return np.array(normalized_features), song_names


def reduce_dimensions(feature_matrix, n_components=10):
    """
    Parameters:
        feature_matrix (np.ndarray): Feature matrix.

    Returns:
        reduced_features (np.ndarray): Dimensionality-reduced features.
    """
    umap = UMAP(n_components=n_components, random_state=42)
    return umap.fit_transform(feature_matrix)


def recommend_songs(song_name, features, song_names, top_n=10):
    """
    Parameters:
        song_name (str): Anchor song name (basis for recommendation).
        features (np.ndarray): Feature matrix.
        song_names (list): List of song names.
        top_n (int): Number of recommendations.

    Returns:
        recommendations (list): List of recommended song names.
    """
    song_idx = song_names.index(song_name)
    distances = cdist(features[song_idx].reshape(1, -1), features, metric='euclidean').flatten()
    recommendations = np.argsort(distances)[1:top_n + 1]
    return [song_names[idx] for idx in recommendations]
