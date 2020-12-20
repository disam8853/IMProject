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
SW_COUNT = 7000
WAIT_FOR_CALCULATE = True

def run_topo():
    global SW_COUNT, WAIT_FOR_CALCULATE
    # global WAIT_FOR_CALCULATE
    # jz = 0
    # while WAIT_FOR_CALCULATE:
    #     jz += 1
    #     print("wait", jz, WAIT_FOR_CALCULATE)
    #     time.sleep(1)
    # with open("./run_topo.py", "r") as f:
        # exec(f.read())
    SW_COUNT += 100
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


@app.route("/CalPath", methods=["POST"])
def calculate_path():
    global WAIT_FOR_CALCULATE
    data = request.json
    try:
        response = run_deploy(config_loc = None, req = data)
        if response == "success":
            show_path(config_loc = None, req = data)
            with open("./path/result.json", "r") as jsfile:
                data = json.load(jsfile)
            # output = ""
            output = {'data': []}
            cnt = 0
            for key in data.keys():
                cnt += 1
                # output += key + ":<br>"
                output['data'].append(
                    {"name": 'Path ' + str(cnt), 'paths': []})
                for i in range(len(data[key]["capacity"])):
                    # output += str(data[key]["link"][i]) + "&nbsp;=(" + \
                    #    str(data[key]["capacity"][i]) + ")=>&nbsp;"
                    output['data'][-1]['paths'].append(
                        {'link': str(data[key]["link"][i]), 'capacity': str(data[key]["capacity"][i])})
                # output += str(data[key]["link"][-1]) + "<br><br>"
                output['data'][-1]['paths'].append(
                    {'link': str(data[key]["link"][-1]), 'capacity': ''})
            # return output
            WAIT_FOR_CALCULATE = False
            
            p2 = threading.Thread(target = run_topo)
             # app.run()
            p2.start()
            print(output)
            while WAIT_FOR_CALCULATE:
                time.sleep(1)
            WAIT_FOR_CALCULATE = True
            return make_response(jsonify(output), 200)
        else:
            return make_response(jsonify({"error": "failed"}), 500)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something Wrong"}), 500)


if __name__ == "__main__":
    
    app.run()

    # p1.join()
    # p2.join()

# @app.route("/showPath", methods=["POST"])
# def showPath():

#     with open("./path/result.json") as jsfile:
#         data = json.load(jsfile)
#     response = ""
#     for key in data.keys():
#         response += key + ":<br>"
#         for i in range(len(data[key]['capacity'])):
#             response += str(data[key]["link"][i]) + "&nbsp=(" + \
#                 str(data[key]["capacity"][i]) + ")=>&nbsp"
#         response += str(data[key]["link"][-1]) + "<br><br>"
#     return response

