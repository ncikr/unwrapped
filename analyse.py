# %% 
# libraries

import pandas as pd
import datetime as dt

# %% #############################################################
## read data

data = pd.read_csv("data\data.csv")

# format dates
data['datetime'] = pd.to_datetime(data['datetime'])
data['year'] = data['datetime'].dt.strftime('%Y')
data['month'] = data['datetime'].dt.strftime('%m')

# %% #############################################################
## total playtime 

# convert ms to hours
data['playtime'] = data['ms_played'] / 3600000

# group and sum playtime
total = data[["month", "year","playtime"]].groupby(["month","year"])["playtime"].sum().reset_index()

# sort
total = total.sort_values(['year', 'month'], ascending= [False,True])

# cumulative sum
total['playtime_cumulative'] = total.groupby(["year"])['playtime'].cumsum()

total['period'] = pd.to_datetime("01-" + total['month'] + "-" + total['year'], dayfirst = True)


# %% #############################################################
## top 25 artists per year 

# group and sum playtime
artists = data[["year","artist","ms_played"]].groupby(["year","artist"])["ms_played"].sum().reset_index()

# rank playtime
artists["year_rank"] = artists.groupby(["year"])["ms_played"].rank(method = "dense", ascending=False)

# filter to top 25
artists = artists[artists["year_rank"] <= 25]

# %% #############################################################
## top 25 tracks per year 

# group and sum playtime
tracks = data[["year","track","ms_played"]].groupby(["year","track"])["ms_played"].sum().reset_index()

# rank playtime
tracks["year_rank"] = tracks.groupby(["year"])["ms_played"].rank(method = "dense", ascending=False)

# filter to top 25
tracks = tracks[tracks["year_rank"] <= 25]


# %% #############################################################
## visualise total

import plotly.express as px
import plotly.io as pio

total['month_label'] = total['period'].dt.strftime('%b')

total = total[total['year'].astype("int") > max(total['year'].astype("int"))-5]


total_fig = px.area(
    total,
    x = "month_label",
    y = "playtime_cumulative",
    color = "year",
    facet_row = "year",
    line_shape = "spline",
    height = 1000,

)

total_fig.layout.template = "plotly_dark+presentation+xgridoff"
total_fig = total_fig.update_xaxes(title = None)
total_fig = total_fig.update_yaxes(title = None)


total_fig.show()


