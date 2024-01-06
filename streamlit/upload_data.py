import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(
    page_title="Unwrapped",
    page_icon="🎧",
)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png",
         width = 100)
st.title("Spotify Unwrapped")
st.header("Unwrap your listening history")

st.file_uploader("Upload your spotify streaming history files (provided by Spotify in JSON format):", accept_multiple_files=True)
st.write("You can download your entire spotify listening history [here](https://www.spotify.com/ca-en/account/privacy/).")

st.button("Upload")

