import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# credentials
os.environ['SPOTIPY_CLIENT_ID'] = st.secrets["spotipy_id"]
os.environ['SPOTIPY_CLIENT_SECRET'] = st.secrets["spotipy_secret"]


st.title("Test app")

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()

for idx, item in enumerate(results['items']):

    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

artist = sp.artist("066X20Nz7iquqkkCW6Jxy6")
st.write(artist)

track = results['items']
st.write(track)
