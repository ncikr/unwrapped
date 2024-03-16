 # libraries

import os 
import json
import pandas as pd

# initialise variables

path = os.getcwd() + "\\data"

data = pd.DataFrame()

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

# drop sensitive cols
data = data.drop(['username', 'platform', 'ip_addr_decrypted', 'user_agent_decrypted'], axis = 1)

# save as csv

data.to_csv("streamlit//my_data.csv")