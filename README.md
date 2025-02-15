# SRecomByFeature
##### Spotify has deprecrated the recommendations endpoint so the daily playlists are now to be manually added to a user-owned single playlist inside the Spotify app
Recommend songs based on audio features from playlists based on user's short-term top tracks and create a playlist with the recommendations.

# Usage
This downloads the songs using [spotify-dl](https://pypi.org/project/spotify-dl/) to extract its audio features (Deleted after), an appropriate amount of storage space is required depending on how many songs there are in the playlist  


  
A Client ID and Client Secret is needed from a [Spotify Developer Account](https://developer.spotify.com/)

navitage to the project directory and run the script, using the command:  
`python srecom.py link-to-the-playlist`.  
The generated playlist will be named 'Generated Playlist'  

The entire process could take up to minutes depending on how large the playlist is





