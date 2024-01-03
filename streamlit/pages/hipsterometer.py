import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(
    page_title="Hipster-o-meter",
    page_icon="😎",
)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png",
         width = 100)
st.title("Spotify Unwrapped")
st.header("How hipster are you?")