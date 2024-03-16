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
st.header("Your Top 100 Artists")


if "data" not in st.session_state or st.session_state.data is None:
    st.error("Please upload your listening history or check the 'testing' box in the 'Upload your data' tab.")

else:
    data = st.session_state.data

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        selection = st.radio("Choose an option:", ["Artists", "Tracks"])

    with col2:
        data = date_filter(data)

    ## Artists ##

    artists = data[["year","artist","hours_played"]].groupby(["artist"])["hours_played"].sum().reset_index()

    # rank playtime
    artists["rank"] = artists["hours_played"].rank(method = "dense", ascending=False)
    artists.hours_played = round(artists.hours_played, 1)

    # filter to top 100
    artists = artists[artists["rank"] <= 100].sort_values(by=['rank'])

    # get history chart
    n_dates = data.datetime.dt.date.unique().shape[0]

    if n_dates < 100:
        data['period'] = data.datetime.dt.date
    else:
        if n_dates < 1000:
            data['period'] = data['datetime'].dt.strftime('%Y') + data['datetime'].dt.strftime('%m')
        else:
            data['period'] = data['datetime'].dt.strftime('%Y')

    artists_history = data[data['artist'].isin(artists['artist'])]    
    artists_history = artists_history[["period","artist","hours_played"]].groupby(["period", "artist"])["hours_played"].sum().reset_index()
    artists_history.hours_played = round(artists_history.hours_played, 2)
    
    max_history = max(artists_history.hours_played)
    min_history = min(artists_history.hours_played)

    artists_history = artists_history.pivot(index = "artist", columns = "period", values = "hours_played").fillna(0)
    artists_history['listening_history'] = artists_history.values.tolist()
    artists_history = artists_history['listening_history'].reset_index()

    # merge history with top 100
    artists = artists.merge(artists_history, on = 'artist', how = 'left')

    ## Tracks ##

    # group and sum playtime
    tracks = data[["year","artist","track","hours_played"]].groupby(["artist","track"])["hours_played"].sum().reset_index()

    # rank playtime
    tracks["rank"] = tracks["hours_played"].rank(method = "dense", ascending=False)
    tracks.hours_played = round(tracks.hours_played, 1)

    # filter to top 100
    tracks = tracks[tracks["rank"] <= 100].sort_values(by=['rank'])

    ## display ##
        
    if selection == "Artists":
         st.data_editor(
            artists[['rank', 'artist', 'hours_played', 'listening_history']],
            column_config={
            "rank": "Rank",
            "artist": "Artist",
            "hours_played": "Hours",
            "listening_history": st.column_config.LineChartColumn(
            "Listening history over period",
            width="medium",
            help="Historical listening trend",
            y_min=min_history,
            y_max=max_history,
         )
        },
        width = 1000,
        height = 3550,
        hide_index=True,
        )

    if selection == "Tracks":
         st.data_editor(
            tracks[['rank', 'track', 'artist', 'hours_played']],
            column_config={
            "Rank": "rank",
            "Track": "track",
            "Artist": "artist",
            "Hours Played": "hours_played"
        },
        width = 1000,
        height = 3600,
        hide_index=True,
        )

if st.session_state.use_my_data:
    st.warning("Testing mode enabled with Nick's listening history")
