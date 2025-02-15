from spotClient import sp

# Get playlist ID by name
def get_playlist_id(playlist_name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            return playlist['id']
    return None

# Get tracks from the playlist
def save_playlist_links(playlist_name, filename="playlist_links.txt"):
    playlist_id = get_playlist_id(playlist_name)
    if not playlist_id:
        print(f"Playlist '{playlist_name}' not found.")
        return
    
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    with open(filename, "w") as file:
        for item in tracks:
            track = item['track']
            url = track['external_urls']['spotify']
            file.write(url + "\n")
    
    print(f"Saved {len(tracks)} links to {filename}")

save_playlist_links("daily")
