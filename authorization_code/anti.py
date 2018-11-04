import spotipy
import sys
import discogs_client
import spotipy.oauth2 as oauth2
import spotipy.util as util
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.request import urlopen
from bs4 import BeautifulSoup


#url = sys.argv
url = input("Paste Playlist URL\n")
type(url)


split_url = url.split("/")

playlist_info = split_url[6]
id_end_index = playlist_info.find("?")

playlist_id = playlist_info[:id_end_index]
username = split_url[4]

client_id = '70ce61b3518c4b68a9b583e1f9e971b4'
client_secret = '36b26da39113479dac1f38743ada505f'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def generate_token():
    """ Generate the token. Please respect these credentials :) """
    credentials = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    token = credentials.get_access_token()
    return token


token = util.prompt_for_user_token(username, scope="playlist-read-private", client_id=client_id, client_secret=client_secret, redirect_uri='https://example.com/callback/')
#token = generate_token()
if token:
    #sp = spotipy.Spotify(auth=token)
    results = spotify.user_playlist(username, playlist_id)
    songs = results["tracks"]
    # List of song ids 
    ids = list()
    # List of artist objects
    artists = list()
    # List of search results from which genres are to be extracted 
    genres = list()
    # List of artist names
    names = list()
    # Dictionary of genres : list of anti-genres 
    antis = dict() 

    #songnames = list()
    #songgenres = list()

    #Find a list of all track ids in the playlist 
    for i, item in enumerate(songs["items"]):
        song = item["track"]
        ids.append(song["id"])
        artists.append(song["artists"])
        #songnames.append(song["name"])
    while songs['next']:
        songs = sp.next(songs)
        for i, item in enumerate(songs["items"]):
            song = item["track"]
            ids.append(song["id"])
            artists.append(song["artists"])
            #songnames.append(song["name"])
    # key = "rMSSoUTCGrIYupZvSiEe"
    # secret = "EVxsbFqVAIFpqIuQWswsUBCzKeKncxWo"
    # d = discogs_client.Client('ExampleApplication/0.1', user_token = 'PGtPrKkPRHNwSSkSEnDAUrothkMjdsoPczOyeeYu')
    # for name in songnames:
    #     result = d.search(name)
    #     genre = result[0].data.get("genre")
    #     songgenres.append(genre)
    # print(songgenres)

    # List of track objects
    all_tracks = spotify.tracks(ids)
    # Find each artist's name for later searching
    for artist in artists:
    	names.append(artist[0].get("name"))

    # Search for every artist's name and append the name to "genres"
    for name in names: 
    	genre = spotify.search(name, limit = 1, type="artist")
    	genres.append(genre)

   	# Find the actual genre of every item in genres 
    for artist in genres:
    	# Remove the 0 to get a list of the artist's genres instead of just the first one 
        most_common_genre = np.random.choice(artist.get("artists").get("items")[0].get('genres')).replace(" ", "").replace("-", "")
        print(most_common_genre)
        quote_page = 'http://everynoise.com/engenremap-'+ most_common_genre + '.html'
        page = urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        holder = list()
        if most_common_genre in antis.keys():
        	holder = antis.get(most_common_genre)
        else: 
            for div in soup.findAll('div', attrs={'id':'mirror'}):
                holder.extend(div.text.replace("»", "").strip().split("\n"))
            antis[most_common_genre] = holder
        print(antis.get(most_common_genre))

else:
    print("Can't get token for", username)






