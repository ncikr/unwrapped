import streamlit as st
import pandas as pd
import datetime as dt
from helpers import *

st.set_page_config(
    page_title="Unwrapped",
    page_icon="🎧",
)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png",
         width = 100)
st.title("Spotify Unwrapped")
st.header("Unwrap your listening history from the beginning of time")


# Upload data

files = st.file_uploader("Upload your spotify streaming history files (JSON only):", 
                         accept_multiple_files=True,
                         help = "You can download your entire spotify listening history [here](https://www.spotify.com/ca-en/account/privacy/).")

exclude_incognito = st.checkbox("Exclude tracks listened to in incognito mode")

uploaded = False

if st.button("Upload"):

    data_raw = load_json_files(files)

    st.session_state.data = data_preprocess(data_raw, exclude_incognito)

    data = st.session_state.data

    summary = data_summary(data)

    st.info(f"Successfully uploaded {summary['plays']} plays from {summary['albums']} unique albums by {summary['artists']} unique artists in {summary['months']} months.")
    
    uploaded = True

    # st.dataframe(data)


if not uploaded:
    st.info("Waiting for Spotify to send you your data? Test the app with my listening history:")

    if "use_my_data" not in st.session_state:
        use_my_data_value = False
    
    else:
        use_my_data_value = st.session_state.use_my_data

    st.session_state.use_my_data = st.toggle("Test this app using Nick's listening history", value = use_my_data_value)

    if st.session_state.use_my_data:
        data_raw = pd.read_csv("streamlit/my_data.csv")
        st.session_state.data = data_preprocess(data_raw, exclude_incognito)

    if not st.session_state.use_my_data:
        st.session_state.data = None

st.markdown("Built by Nick Ross ([Link to Github profile](https://github.com/ncikr))")
        