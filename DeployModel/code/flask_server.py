# this is the backend of GUI (orchestrator)
# open server at port 5000

import flask
from flask import jsonify, request, make_response
from flask_cors import CORS
import os
import json
from flask_main import *
from show_path import *
import random
import math
import numpy as np
from Class import *
from LR import LR
import time
import sys
from catknight import *
import threading

app = flask.Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
SW_COUNT = 7000 # virtual switch's initial ID
WAIT_FOR_CALCULATE = True # wait until topology is set

def run_topo():
    # WAIT_FOR_CALCULATE = True # if there's some error, remove this line.
    global SW_COUNT, WAIT_FOR_CALCULATE
    SW_COUNT += 100

    # execute run_topo.py to generate virtual topology
    os.system("sudo python3 ./run_topo.py")
    WAIT_FOR_CALCULATE = False

@app.route('/test', methods=['GET'])
def test():
    return 'test'


@app.route('/getAdjMatrix', methods=['GET'])
def get_adj_matrix():
    if os.path.exists('adjacency.csv'):
        adjacency_matrix = []
        file = open('adjacency.csv')
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


@app.route('/getJsonLink/<json_file>', methods=['GET'])
def get_json_link(json_file):
    # get links from link.csv
    if os.path.exists('link.csv'):
        links = []
        file = open('link.csv')
        link_list = file.readlines()
        link_list = link_list[1:]
        for link in link_list:
            link = list(map(int, (link[: -1]).split(',')))[1:]
            links.append(link)
        file.close()

        if os.path.exists(f'path/{json_file}'):
            file = open(f'path/{json_file}')
            path = file.read()
            path = json.loads(path)
            methods = []
            keys = path.keys()
            for key in keys:
                methods.append(path[key])
            return jsonify({'link': links, 'path': methods})

# execute CalPath to trigger algorithm of deploy model
@app.route("/CalPath", methods=["POST"])
def calculate_path():
    global WAIT_FOR_CALCULATE
    data = request.json
    try:
        # trigger algorithm
        response = run_deploy(config_loc = None, req = data)
        if response == "success":
            # change output.txt to a better format for human & code
            show_path(config_loc = None, req = data)
            with open("./path/result.json", "r") as jsfile:
                data = json.load(jsfile)
            output = {'data': []}
            cnt = 0

            # make json data for frontend
            for key in data.keys():
                cnt += 1
                # output += key + ":<br>"
                output['data'].append(
                    {"name": 'Path ' + str(cnt), 'paths': []})
                for i in range(len(data[key]["capacity"])):
                    output['data'][-1]['paths'].append(
                        {'link': str(data[key]["link"][i]), 'capacity': str(data[key]["capacity"][i])})
                output['data'][-1]['paths'].append(
                    {'link': str(data[key]["link"][-1]), 'capacity': ''})
            WAIT_FOR_CALCULATE = False
            
            # use multithread to set topology from links.csv and adjacency.csv
            p2 = threading.Thread(target = run_topo)
            p2.start()
            print(output)
            while WAIT_FOR_CALCULATE:
                time.sleep(1)
            WAIT_FOR_CALCULATE = True # wait until run_topo.py done
            return make_response(jsonify(output), 200)
        else:
            # fail while calculate best path
            return make_response(jsonify({"error": "failed"}), 500)
    except Exception as e:
        # if there're some bugs...
        print(e)
        return make_response(jsonify({"error": "Something Wrong"}), 500)


if __name__ == "__main__":
    app.run()

