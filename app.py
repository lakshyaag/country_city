from flask import Flask, render_template, request

import web_play

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play', methods=['POST'])
def play():
    name = request.form['name']
    location = request.form['location']
    continent = request.form['continent']

    countries = web_play.get_countries(continent)

    return render_template('play.html', name=name, continent=continent, location=location,
                           cont=web_play.get_country(iter(countries)))


if __name__ == "__main__":
    app.run()
