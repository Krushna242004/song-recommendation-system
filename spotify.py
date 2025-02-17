#This code is used to fetch the links of songs.

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "e73dfb26a6464195a80a3af89cbc2026"  
CLIENT_SECRET = "52648da88598403299b2b6c9ffb5f4b1"  

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the CSV file
csv_file = "spotify_millsongdata.csv"
df = pd.read_csv(csv_file)

# Add a new column for Spotify Links
df['spotify_link'] = None

# Function to fetch Spotify track link
def get_spotify_link(song_name, artist_name):
    try:
        query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=query, type="track", limit=1)
        if results['tracks']['items']:
            return results['tracks']['items'][0]['external_urls']['spotify']
        else:
            return None
    except Exception as e:
        print(f"Error fetching link for {song_name} by {artist_name}: {e}")
        return None

# Iterate over each row and fetch Spotify link
for index, row in df.iterrows():
    song = row['song']
    artist = row['artist']
    if pd.notna(song) and pd.notna(artist):  
        link = get_spotify_link(song, artist)
        df.at[index, 'spotify_link'] = link
        print(f"Processed: {song} by {artist}")

# Save the updated CSV
df.to_csv("updated_spotify_millsongdata.csv", index=False)
print("CSV updated with Spotify links.")
