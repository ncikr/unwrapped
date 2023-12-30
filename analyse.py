# %% 
# libraries

import pandas as pd
import datetime as dt

# %%
# read data

data = pd.read_csv("data\data.csv")

# format dates
data['datetime'] = pd.to_datetime(data['datetime'])

# %%
# top 50 artists
data['year'] = data['datetime'].dt.strftime('%Y')

artists = data.groupby(["year","artist"]).size()



