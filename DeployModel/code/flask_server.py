import flask
from flask import jsonify
from flask_cors import CORS
import os

app = flask.Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

@app.route('/test', methods = ['GET'])
def test():
	return 'test'

@app.route('/getAdjMatrix', methods = ['GET'])
def get_adj_matrix():
	if os.path.exists('adjacency.txt'):
		adjacency_matrix = []
		file = open('adjacency.txt')
		all_rows = file.readlines()
		for row in all_rows:
			row = row[:-1].split(',')
			for i in range(len(row)):
				row[i] = int(row[i])
			adjacency_matrix.append(row)
		file.close()
		return jsonify(adjacency_matrix)
	else:
		return jsonify({'matrix': []})

app.run()