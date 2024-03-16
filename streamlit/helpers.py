import json
import pandas as pd
import streamlit as st
import datetime as dt


def load_json_files(files):

    # load json and convert to df

    data = pd.DataFrame()

    for file in files:
        temp = pd.DataFrame(json.load(file))
        data = pd.concat([data, temp])

    return data

def data_preprocess(data, exclude_incognito):

    # filter to non-incognito plays
    if exclude_incognito:
        data = data[data.incognito_mode == False]

    # rename cols
    data = data.rename(columns = {'ts':'datetime',
                                'master_metadata_track_name':'track',
                                'master_metadata_album_artist_name':'artist', 
                                'master_metadata_album_album_name':'album'})
    
    # remove podcasts
    data = data[data.episode_name.isnull()]
    
    # formate datetime
    data.datetime = pd.to_datetime(data.datetime)
    data['year'] = data.datetime.dt.year.astype("string")
    data['month'] = data.datetime.dt.month.astype("string")

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

    year_selection = st.selectbox("Select a period:", year_options)

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
            date_from = dt.date(pd.to_numeric(year_selection),1,1)
            date_to = dt.date(pd.to_numeric(year_selection),12,31)

    data_filtered = data[pd.to_datetime(data['datetime']).dt.date >= date_from]
    data_filtered = data_filtered[pd.to_datetime(data_filtered['datetime']).dt.date <= date_to]

    return data_filtered


def get_listening_history(data, data_top100, grouping = ['artist','track']):

    # set time units based on length of period   
    n_dates = data.datetime.dt.date.unique().shape[0]

    if n_dates < 100:
        data['period'] = data.datetime.dt.date
    else:
        if n_dates < 1000:
            data['period'] = data['datetime'].dt.strftime('%Y') + data['datetime'].dt.strftime('%m')
        else:
            data['period'] = data['datetime'].dt.strftime('%Y')

    # group and summarise history        
            
    if grouping == "artist":
        filter_variables = ["period","artist","hours_played"]
        grouping_variables = ['period','artist']
        pivot_index = ['artist']

    if grouping == 'track':
        filter_variables = ["period","track","artist","hours_played"]
        grouping_variables = ['period','artist', 'track']
        pivot_index = ['artist', 'track']


    data_with_history = data[data[grouping].isin(data_top100[grouping])]    
    data_with_history = data_with_history[filter_variables].groupby(grouping_variables)["hours_played"].sum().reset_index()
    data_with_history.hours_played = round(data_with_history.hours_played, 2)
    
    max_history = max(data_with_history.hours_played)
    min_history = min(data_with_history.hours_played)

    data_with_history = data_with_history.pivot(index = pivot_index, columns = "period", values = "hours_played").fillna(0)
    data_with_history['listening_history'] = data_with_history.values.tolist()
    data_with_history = data_with_history['listening_history'].reset_index()

    return data_with_history, max_history, min_history
