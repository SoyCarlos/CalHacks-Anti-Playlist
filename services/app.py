import spotipy
import sys
import discogs_client
import spotipy.oauth2 as oauth2
import spotipy.util as util
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from json.decoder import JSONDecodeError
import json

def anti(playlist_url, user_id, token, playlist_name="125125125"):
    url = playlist_url

    split_url = url.split("/")

    playlist_info = split_url[6]
    id_end_index = playlist_info.find("?")

    playlist_id = playlist_info[:id_end_index]
    username = split_url[4]
    key_file = "keys.json"
    keys = json.load(open(key_file))
    client_id = keys["client_id"]
    client_secret = keys["client_secret"]

    # client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    # spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # try:
    #     token = util.prompt_for_user_token(username, "playlist-modify-public", client_id, client_secret, redirect_uri='http://localhost/')
    # except (AttributeError, JSONDecodeError):
    #     os.remove(f".cache-{username}")
    #     token = util.prompt_for_user_token(username, "playlist-modify-public", client_id, client_secret, redirect_uri='http://localhost/')

    

    if token:
        spotify = spotipy.Spotify(auth=token, requests_timeout=20)
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
        # Dictionary of artists: genres
        artistgenres = dict() 
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
            try:
                genre = spotify.search(name, limit = 1, type="artist")
                genres.append(genre)
            except:
                continue

        # Find the actual genre of every item in genres 
        for artist in genres:
            # Remove the 0 to get a list of the artist's genres instead of just the first one 
            artist_genres = artist.get("artists").get("items")[0].get('genres')
            # i = 0
            # while artist_genres == [] and i < len(artist.get("artists").get("items")):
            # 	artist_genres = artist.get("artists").get("items")[i].get('genres')
            # 	i+= 1
            if artist_genres == []:
                continue
            most_common_genre = np.random.choice(artist_genres).replace(" ", "").replace("-", "").replace("+", "").replace("'", "").replace("&", "")
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
            curr_anti = np.random.choice(antis.get(most_common_genre)).replace(" ", "").replace("-", "").replace("+", "").replace("'", "").replace("&", "")
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
                curr_anti = np.random.choice(antis.get(most_common_genre)).replace(" ", "").replace("-", "").replace("+", "").replace("'", "").replace("&", "")
                #print(curr_anti)
                quote_page = 'http://everynoise.com/engenremap-'+ curr_anti + '.html'
                page = urlopen(quote_page)
                soup = BeautifulSoup(page, 'html.parser')
                anti_artists = list()
                for div in soup.findAll('div', attrs={"class": "canvas"}):
                    anti_artists.extend(div.text.replace("»", "").strip().split("\n"))

                selected_anti = np.random.choice(anti_artists)
                #print(selected_anti)
                try:
                    anti_object = spotify.search(selected_anti, limit = 1, type="artist")
                except:
                    continue
                anti_artistoo = anti_object.get("artists").get("items")
                for i in range(50):
                    if len(anti_artistoo) == 0: 
                        selected_anti = np.random.choice(anti_artists)
                        try:
                            anti_object = spotify.search(selected_anti, limit = 1, type="artist")
                        except:
                            continue
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
                name = song.get("name")#.get('name')
                songid = song.get("id")#.get("id")
                songuri = song.get("uri")#.get("uri")
                #print(name, songid, songuri)
                top10songs.append(name)
                top10ids.append(songid)
                top10uris.append(songuri)
                #print(top10songs)
            if len(top10songs) == 0:
                continue
            songindex = np.random.choice(len(top10songs))
            final[top10songs[songindex]] = top10ids[songindex]
        print(final)
        userid = user_id
        newname = playlist_name
        newplaylist = spotify.user_playlist_create(userid, newname)
        result = spotify.user_playlist_add_tracks(userid, newplaylist.get("id"), list(final.values()))
        print(result)
        for filename in os.listdir("."):
            if filename.startswith(".cache-"):
                os.remove(filename)


    else:
        print("Can't get token for", username)


def spotipy_auth(url):

    url = url

    split_url = url.split("/")

    username = split_url[4]

    key_file = "keys.json"
    keys = json.load(open(key_file))
    client_id = keys["client_id"]
    client_secret = keys["client_secret"]

    try:
        token = util.prompt_for_user_token(username, "playlist-modify-public", client_id, client_secret, redirect_uri='http://localhost/')
        return token
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, "playlist-modify-public", client_id, client_secret, redirect_uri='http://localhost/')
