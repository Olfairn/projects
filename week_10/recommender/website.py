from flask import Flask
import recommender
from flask.templating import render_template

app = Flask('Flo movie recommender')

@app.route('/movie')
def get_movie():
    movie = recommender.get_movie_reco()
    return render_template('movie.html', movie=movie, score=0.22)


@app.route('/')
def hello():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)