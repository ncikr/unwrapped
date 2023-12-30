 
#%% 
# libraries

import os 
import json
import pandas as pd

# %%
# initialise variables

path = os.getcwd() + "\\data"

data = pd.DataFrame()

# %%
# read and combine files

# iterate through all file 
for file in os.listdir(path): 
    # Check whether file is in json format or not 
    if file.endswith(".json"): 
        file_path = path + "\\" + file

        f = open(file_path)
        temp = pd.DataFrame(json.load(f))

        data = pd.concat([data, temp])

        f.close()

# %%
# rename and filter columns
        
data = data.rename(columns = {'ts':'datetime',
                              'master_metadata_track_name':'track',
                              'master_metadata_album_artist_name':'artist', 
                              'master_metadata_album_album_name':'album'})
        
data = data[['datetime','ms_played','track',
            'artist', 'album','reason_start',
            'reason_end', 'shuffle','skipped']]

# %%
# save as csv

data.to_csv("data//data.csv")