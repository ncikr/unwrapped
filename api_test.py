#%% libraries

import spotipy
from spotipy.oauth2 import SpotifyOAuth


#%%

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()

for idx, item in enumerate(results['items']):

    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])


# %%

artist = sp.artist("066X20Nz7iquqkkCW6Jxy6")
print(artist)


# %%

track = results['items']

# %%