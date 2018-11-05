from flask import Flask, request, render_template, redirect, url_for, session
from services.app import anti, spotipy_auth, authenicate_spotipy
import json

app = Flask(__name__)
app.secret_key = 'Im trying my best'

auth = []

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/playlist_url', methods=['POST', 'GET'])
def playlist_url():
    if request.method == 'POST':
        session['p_url'] = request.form['playlist_url']

    return render_template("second.html")

def authenticate():
    return spotipy_auth(session['p_url'])

@app.route('/pre_redirect_url', methods=['POST', 'GET'])
def pre_redirect_url():
    return render_template("redirect_uri.html")

@app.route('/redirect_url', methods=['POST', 'GET'])
def redirect_url():
    auth.append(authenticate())
    print(auth)
    if request.method == 'POST':
        user_uri = request.form['user_uri']
        user_id = user_uri.split('spotify:user:')[1]
        session['user_id'] = user_id


    return render_template("redirect_uri.html")

@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        session['redirect_url'] = request.form['redirect']
    
    session['token'] = authenicate_spotipy(session['redirect_url'], auth[0])

    anti(session['p_url'], session['user_id'], session['token'])

    return render_template("results.html")

if __name__ == '__main__':
   app.run(debug = True)

