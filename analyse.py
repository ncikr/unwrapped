# %% 
# libraries

import pandas as pd
import datetime as dt

# %%
# read data

data = pd.read_csv("data\data.csv")

# format dates
data['datetime'] = pd.to_datetime(data['datetime'])
data['year'] = data['datetime'].dt.strftime('%Y')
data['month'] = data['datetime'].dt.strftime('%m')

# %%
## total playtime ##

# group and sum playtime
total = data[["month", "year","ms_played"]].groupby(["month","year"])["ms_played"].sum().reset_index()

# sort
total = total.sort_values(['year', 'month'], ascending=True)

# cumulative sum
total['ms_played_cumulative'] = total.groupby(["year"])['ms_played'].cumsum()


# %%
## top 25 artists per year ##

# group and sum playtime
artists = data[["year","artist","ms_played"]].groupby(["year","artist"])["ms_played"].sum().reset_index()

# rank playtime
artists["year_rank"] = artists.groupby(["year"])["ms_played"].rank(method = "dense", ascending=False)

# filter to top 25
artists = artists[artists["year_rank"] <= 25]

# %%
## top 25 tracks per year ##

# group and sum playtime
tracks = data[["year","track","ms_played"]].groupby(["year","track"])["ms_played"].sum().reset_index()

# rank playtime
tracks["year_rank"] = tracks.groupby(["year"])["ms_played"].rank(method = "dense", ascending=False)

# filter to top 25
tracks = tracks[tracks["year_rank"] <= 25]
# %%
