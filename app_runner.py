from flask import Flask, request, render_template, redirect, url_for, session
from services.app import anti, spotipy_auth
from celery import Celery

app = Flask(__name__)
app.secret_key = 'Im trying my best'

app.config['CELERY_BROKER_URL'] = 'localhost:5000'
app.config['CELERY_RESULT_BACKEND'] = 'localhost:5000'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def authenticate():
    return spotipy_auth(session['p_url'])

@app.route('/')
def index():
    if 'p_url' in session:
        print("Hell yeah sessions")
        print(session['p_url'])
    return render_template("index.html")


@app.route('/playlist_url', methods=['POST', 'GET'])
def playlist_url():
    if request.method == 'POST':
        session['p_url'] = request.form['playlist_url']
    print(session['p_url'])
    return render_template("second.html")

@app.route('/redirect_url', methods=['POST', 'GET'])
def redirect_url():
    if request.method == 'POST':
        user_uri = request.form['user_uri']
        user_id = user_uri.split('spotify:user:')[1]
        session['user_id'] = user_id

    session['token'] =  authenticate.delay()
    return render_template("redirect_uri.html")

@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        session['redirect_url'] = request.form['redirect']
    
    print("Authenticating")
    print("Authenticated")
    
    print('Playlist URL: ' + session['p_url'])
    print('User ID: ' + session['user_id'])
    print('Redirect: ' + session['redirect_url'])

    

    print("calling anti ya yeet")
    anti(session['p_url'], session['user_id'], session['token'])
    print("called anti")
    return render_template("results.html")

if __name__ == '__main__':
   app.run(debug = True)

