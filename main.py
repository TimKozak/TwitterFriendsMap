from flask import Flask, render_template, request, redirect, url_for
from tools import get_coordinates, generate_map, twitter_api

app = Flask(__name__)


@app.route('/home', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form.get('token')
        user = request.form.get('user')
        try:
            data = twitter_api(user, token)
            return render_template(generate_map(get_coordinates(data)))
        except KeyError:
            return redirect(url_for('failure'))

    return render_template('index.html')


@ app.route('/failure', methods=["GET", "POST"])
def failure():
    if request.method == "POST":
        return redirect(url_for('index'))
    return render_template('fail.html')


if __name__ == "__main__":
    app.run(debug=True)
