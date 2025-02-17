import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from scipy.sparse import load_npz
import pandas as pd

# Spotify Client Credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Hardcoded username and password
VALID_USERNAME = "krushna"
VALID_PASSWORD = "pass123"

# Function to fetch album cover URL
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    try:
        results = sp.search(q=search_query, type="track")
        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            return track["album"]["images"][0]["url"]
    except Exception as e:
        print(f"Error fetching album cover: {e}")
    return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default image URL

# Recommendation function
def recommend(song, music, similarity_sparse):
    try:
        index = music[music['song'] == song].index[0]
        distances = similarity_sparse[index].toarray()[0]
        sorted_indices = distances.argsort()[::-1][1:7]

        recommended_music_names = []
        recommended_music_posters = []
        recommended_music_links = []
        recommended_music_artists = []

        for i in sorted_indices:
            artist = music.iloc[i].artist
            recommended_music_names.append(music.iloc[i].song)
            recommended_music_posters.append(get_song_album_cover_url(music.iloc[i].song, artist))
            recommended_music_links.append(music.iloc[i].spotify_link)
            recommended_music_artists.append(artist)

        return recommended_music_names, recommended_music_posters, recommended_music_links, recommended_music_artists
    except Exception as e:
        print(f"Error: {e}")
        return [], [], [], []

# Streamlit UI
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login BAJAATE RAHO 🎶")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password!")
else:
    st.header('BAJAATE RAHO 🎶')

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    # Load Data
    try:
        music = pickle.load(open('df.pkl', 'rb'))
        music.dropna(subset=['song', 'artist', 'spotify_link'], inplace=True)
    except Exception as e:
        st.error(f"Error loading df.pkl: {e}")
        st.stop()

    try:
        similarity_sparse = load_npz('similarity_sparse.npz')
    except Exception as e:
        st.error(f"Error loading similarity_sparse.npz: {e}")
        st.stop()

    if 'song' not in music.columns:
        st.error("The 'song' column is missing in the DataFrame.")
        st.stop()

    music_list = music['song'].drop_duplicates().values
    selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters, recommended_music_links, recommended_music_artists = recommend(selected_song, music, similarity_sparse)

        if recommended_music_names:
            cols = st.columns(len(recommended_music_names))
            for i, col in enumerate(cols):
                with col:
                    # Clickable Image
                    link = recommended_music_links[i]
                    image_html = f'<a href="{link}" target="_blank"><img src="{recommended_music_posters[i]}" style="width:100%; border-radius:10px;" /></a>'
                    st.markdown(image_html, unsafe_allow_html=True)
                    
                    # Song Name and Artist
                    st.write(f"**{recommended_music_names[i]}**")
                    st.write(f"*{recommended_music_artists[i]}*")
        else:
            st.text("No recommendations found. Please try a different song.")
