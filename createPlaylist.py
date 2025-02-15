from spotipy.oauth2 import SpotifyOAuth
from spotClient import sp
import re


PLAYLIST_NAME = "Generated Playlist"

# Extracts artist and song name from a line
def parse_song_line(line):
    match = re.match(r"(.+?)\s*[-,]\s*(.+)", line)
    if match:
        return match.group(1), match.group(2)
    return None, None

# Searches for a song on Spotify and returns the first result's URI
def get_song_uri(artist, song):
    query = f"{song} {artist}"
    results = sp.search(q=query, limit=1, type="track")
    tracks = results.get("tracks", {}).get("items", [])
    return tracks[0]["uri"] if tracks else None

# Create new empty Spotify playlist and returns its ID.
def create_playlist():
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, PLAYLIST_NAME, public=True)
    return playlist["id"]


# Populate the new empty Spotify playlist, searches Spotify, and adds songs to the new playlist.
def populate_playlist(song_names):
    song_uris = []
    for line in song_names:
        artist, song = parse_song_line(line)
        if artist and song:
            uri = get_song_uri(artist, song)
            if uri:
                song_uris.append(uri)
                print(f"Added: {artist} - {song}")
            else:
                print(f"Not found: {artist} - {song}")

    if not song_uris:
        print("No songs. Exiting...")
        return

    playlist_id = create_playlist()
    sp.playlist_replace_items(playlist_id, song_uris)
    print(f"Playlist '{PLAYLIST_NAME}' created with {len(song_uris)} songs!")
