from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'Im trying my best'

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

@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        user_uri = request.form['user_uri']
        user_id = user_uri.split('spotify:user:')[1]
        session['user_id'] = user_id
    print('Playlist URL: ' + session['p_url'])
    print('User ID: ' + session['user_id'])
    return render_template("results.html")

if __name__ == '__main__':
   app.run(debug = True)