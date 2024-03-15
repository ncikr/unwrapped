import streamlit as st
import pandas as pd
import datetime as dt
from helpers import date_filter

st.set_page_config(
    page_title="Top 100",
    page_icon="🏆",
)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png",
         width = 100)
st.title("Spotify Unwrapped")
st.header("Ulitmate top 100")


if "data" not in st.session_state or st.session_state.data is None:
    st.error("Please upload your listening history or check the 'testing' box in the 'Upload your data' tab.")

else:
    data = st.session_state.data

    data = date_filter(data)

    # group and sum playtime by year

    artists = data[["year","artist","hours_played"]].groupby(["artist"])["hours_played"].sum().reset_index()

    # rank playtime
    artists["rank"] = artists["hours_played"].rank(method = "dense", ascending=False)

    artists.hours_played = round(artists.hours_played, 1)

    # filter to top 25
    artists = artists[artists["rank"] <= 100].sort_values(by=['rank'])
    
    st.data_editor(
        artists,
         column_config={
        "Rank": "rank",
        "Artist": "artist",
        "Hours Played": "hours_played"
    },
    hide_index=True,
    )


