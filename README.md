# Anti-Playlist

### About The Developers
Anti-Playlist is a web app developed by UC Berkeley Students, Youmna Rabie (@YoumnaRabie), Carlos Eduardo Ortega (@SoyCarloss), Jaydon Leo Krooss (@JayLeoK) and Yasmine Frigui (@YFrigui) during UC Berkeley's 2018 CalHacks Hackathon.

### About Anti-Playlist
Anti-Playlist takes a user's Spotify Playlist URL and uses Glenn McDonald's everynoise.com website to find the "opposite" of as many genres in the playlist as possible. Glenn McDonald's algorithm uses a 12-dimensional analytical space to represent the 12 attributes used, Acousticness, Beat Strength, Bounciness, Danceability, Dynamic Range Mean, Flatness, Energy, Loudness, Mechanism, Organicness, Tempo, Valence).

### How to Run
The first step is to create an account on Spotify's Developer site (http://developer.spotify.com). Then create a file named 'key.json' in the following format:

{
	"client_id": "YOUR CLIENT ID",
	"client_secret": "YOUR CLIENT SECRET",
	"redirect_uri": "YOUR REDIRECT URI"
}

Then run app_runner.py and open localhost:5000/ in your browser of choice. 


### Dependencies
This project requires the following Python modules that don't automatically come installed with Python:
* Flask
* Spotipy
* Discogs
* Numpy
* BeautifulSoup
