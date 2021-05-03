# pip install flask
# python -m pip install flask

import os, json
from flask import Flask, jsonify, request, redirect, render_template
import recommender

app = Flask(__name__)

@app.route('/movie')  # <-- suffix of the URL
def get_movie():
    #TODO read URL parameters
    d = dict(request.args)
    name1 = d['movie1']
    name2 = d['movie2']
    rating1 = int(d['rating1'])
    rating2 = int(d['rating2'])
    dict_name_rating = {name1:rating1,name2:rating2}
    movie = recommender.get_movie_recommendation(dict_name_rating)
    return render_template('main_template.html', 
                           movie=list(movie.keys())[0:12], 
                           title='your recommendations:')

@app.route('/')
def hello():
    return render_template('main_template.html') # in templates/

@app.route('/search', methods=['POST'])
def search():
	term = request.form['q']
	print ('term: ', term)
	
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "results.json")
	json_data = json.loads(open(json_url).read())
	#print (json_data)
	#print (json_data[0])
	
	filtered_dict = [v for v in json_data if term in v]	
	#print(filtered_dict)
	
	resp = jsonify(filtered_dict)
	resp.status_code = 200
	return resp


if __name__ == "__main__":
    app.run(debug=True, port=5000)

