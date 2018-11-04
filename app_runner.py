from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("index.html")


@app.route('/playlist_url', methods=['POST', 'GET'])
def playlist_url():
    if request.method == 'POST':
        p_url = request.form['playlist_url']
        return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug = True)