import json
import pandas as pd
import streamlit as st


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
    data.year = data.datetime.dt.year
    data.month = data.datetime.dt.month

    # select relevant cols        
    data = data[['datetime','ms_played','track',
                'artist', 'album','reason_start',
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
