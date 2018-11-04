import spotipy
import sys
import discogs_client
import spotipy.oauth2 as oauth2
import spotipy.util as util
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

url = input("Paste Playlist URL\n")
type(url)


split_url = url.split("/")

playlist_info = split_url[6]
id_end_index = playlist_info.find("?")

playlist_id = playlist_info[:id_end_index]
username = split_url[4]

client_id = '70ce61b3518c4b68a9b583e1f9e971b4'
client_secret = '36b26da39113479dac1f38743ada505f'

# client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
# spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = util.prompt_for_user_token(username, scope="playlist-modify-public", client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost/', cache_path=None)
#token = generate_token()
if token:
	spotify = spotipy.Spotify(auth=token)
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
	# Dictionary of ids : song names for the final playlist
	final = dict()


    #Find a list of all track ids in the playlist 
	for i, item in enumerate(songs["items"]):
		song = item["track"]
		ids.append(song["id"])
		artists.append(song["artists"])
    # If there are more pages of songs, add them too. 
	while songs['next']:
		songs = sp.next(songs)
		for i, item in enumerate(songs["items"]):
			song = item["track"]
			ids.append(song["id"])
			artists.append(song["artists"])


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
		artist_genres = artist.get("artists").get("items")[0].get('genres')
		most_common_genre = np.random.choice(artist_genres).replace(" ", "").replace("-", "")
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
		curr_anti = np.random.choice(antis.get(most_common_genre)).replace(" ", "").replace("-", "").replace("+", "")
		#print(curr_anti)


        # Go to anti page and find a random artist 
		quote_page = 'http://everynoise.com/engenremap-'+ curr_anti + '.html'
		page = urlopen(quote_page)
		soup = BeautifulSoup(page, 'html.parser')
		anti_artists = list()
		for div in soup.findAll('div', attrs={"class": "canvas"}):
			anti_artists.extend(div.text.replace("»", "").strip().split("\n"))

		selected_anti = np.random.choice(anti_artists)
		#print(selected_anti)
		anti_object = spotify.search(selected_anti, limit = 1, type="artist")
		anti_artistoo = anti_object.get("artists").get("items")
		anti_artist_id = ""
		while len(anti_artist_id) == 0:
			curr_anti = np.random.choice(antis.get(most_common_genre)).replace(" ", "").replace("-", "").replace("+", "")
			#print(curr_anti)
			quote_page = 'http://everynoise.com/engenremap-'+ curr_anti + '.html'
			page = urlopen(quote_page)
			soup = BeautifulSoup(page, 'html.parser')
			anti_artists = list()
			for div in soup.findAll('div', attrs={"class": "canvas"}):
				anti_artists.extend(div.text.replace("»", "").strip().split("\n"))

			selected_anti = np.random.choice(anti_artists)
			#print(selected_anti)
			anti_object = spotify.search(selected_anti, limit = 1, type="artist")
			anti_artistoo = anti_object.get("artists").get("items")
			for i in range(50):
				if len(anti_artistoo) == 0: 
					selected_anti = np.random.choice(anti_artists)
					anti_object = spotify.search(selected_anti, limit = 1, type="artist")
				else: 
					anti_artist_id = anti_artistoo[0].get("id")
					break
        
		#print(anti_artist_id)
		#if anti_artist_id:
		top10 = spotify.artist_top_tracks(anti_artist_id)
    	#print(top10.get("tracks")[1])#.get("album").get("name"))
		top10songs = list()
		top10ids = list()
		top10uris = list()
		for song in top10.get("tracks"):
			name = song.get("album").get('name')
			songid = song.get("album").get("id")
			songuri = song.get("album").get("uri")
			if name in top10songs:
				continue
			else:
				top10songs.append(name)
				top10ids.append(songid)
				top10uris.append(songuri)
			#print(top10songs)
		songindex = np.random.choice(len(top10songs))
		final[top10songs[songindex]] = top10uris[songindex]
	print(final)
	userid = input("What's your user id?\n")
	newname = input("What's your playlist name?\n")
	newplaylist = spotify.user_playlist_create(userid, newname)
	#Take final.values, grab their ids (they're albums), and grab random songs from those albums. grab their ids and add those to playlist
	#result = spotify.user_playlist_add_tracks(userid, newplaylist.get("id"), ",".join(list(final.values())))

	add_tracks = []
	for album in final.values():
		current = spotify.album_tracks(album)
		current_tracks = spotify.album_tracks(album)
		random_index = random.randint(0, len(current_tracks['items']) - 1)
		random_track = current_tracks['items'][random_index]['uri']
		add_tracks.append(random_track)
		

	result = spotify.user_playlist_add_tracks(userid, newplaylist.get("id"), add_tracks)

	print(result)





else:
    print("Can't get token for", username)




