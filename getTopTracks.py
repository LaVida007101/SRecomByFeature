from spotClient import sp

# Get user's top songs
def save_top_tracks(time_range="short_term", limit=7, link_filename="top_tracks.txt", name_filename="top_track_names.txt"):
    # param time_range: "short_term" (4 weeks), "medium_term" (6 months), "long_term" (1 year)

    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    
    with open(link_filename, "w", encoding="utf-8") as link_file, open(name_filename, "w", encoding="utf-8") as name_file:
        for item in results['items']:
            url = item['external_urls']['spotify']
            artists = ", ".join(artist['name'] for artist in item['artists'])
            name = item['name'].replace(':', '#')
            link_file.write(url + "\n")
            name_file.write(f"{artists} - {name}\n")


save_top_tracks(time_range="medium_term", limit=10)