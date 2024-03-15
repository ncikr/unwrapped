import json
import pandas as pd
import streamlit as st
import datetime as dt


def load_json_files(files, exclude_incognito):

    # load json and convert to df

    data = pd.DataFrame()

    for file in files:
        temp = pd.DataFrame(json.load(file))
        data = pd.concat([data, temp])

    # remove podcasts
    data = data[data.episode_name.isnull()]

    # filter to non-incognito plays
    if exclude_incognito:
        data = data[data.incognito_mode == False]

    # rename cols
    data = data.rename(columns = {'ts':'datetime',
                                'master_metadata_track_name':'track',
                                'master_metadata_album_artist_name':'artist', 
                                'master_metadata_album_album_name':'album'})
    
    # formate datetime
    data.datetime = pd.to_datetime(data.datetime)
    data['year'] = data.datetime.dt.year.astype("text")
    data['month'] = data.datetime.dt.month.astype("text")

    # format numeric
    data.ms_played = data.ms_played.astype("int")
    data['hours_played'] = data.ms_played / 3600000

    # select relevant cols        
    data = data[['datetime', 'year', 'month','ms_played','track',
                'hours_played', 'artist', 'album','reason_start',
                'reason_end', 'shuffle','skipped']]

    return data

def data_summary(data):

    summary = {}

    summary['plays'] = data.shape[0]
    summary['albums'] = data.artist.unique().shape[0]
    summary['artists'] = data.album.unique().shape[0]

    year_months = data.year + data.month

    summary['months'] = year_months.unique().shape[0]

    return summary

def date_filter(data):

        # date input
    data['date'] = data.datetime.dt.date
    min_date = min(data.date)
    max_date = max(data.date)

    unique_years = data.year.unique()
    year_options = unique_years.tolist()
    year_options.insert(0, "All time")
    year_options.insert(1, "Date range")

    year_selection = st.selectbox("Select a year:", year_options)

    if year_selection == "Date range":
        
        date_selection = st.date_input(
        "Choose a date range",
        (min_date, max_date),
        min_date,
        max_date,
        format="DD-MM-YYYY",
        )

        date_from = date_selection[0]
        date_to = date_selection[1]

    else:
        if year_selection == "All time":
            date_from = min_date
            date_to = max_date

        else:
            date_from = dt.date(year_selection,1,1)
            date_to = dt.date(year_selection,12,31)

    data_filtered = data[pd.to_datetime(data['datetime']).dt.date >= date_from]
    data_filtered = data[pd.to_datetime(data['datetime']).dt.date <= date_to]

    return data_filtered