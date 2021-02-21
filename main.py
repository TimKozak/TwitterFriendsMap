from flask import Flask, render_template, request
from tools import get_coordinates, generate_map, twitter_api

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user = request.form.get('user')
        return render_template(generate_map(get_coordinates(twitter_api(user))))

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
