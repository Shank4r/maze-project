from flask import Flask, jsonify, request
from flask_cors import CORS
from Utilities import functions as fn
from Utilities.Nodelist import Nodelist

app = Flask(__name__)

CORS(app)

nodeList = Nodelist()


@app.route('/getMaze', methods=['POST'])
def getMaze():
    map = request.get_json()["map"]
    start = request.get_json()["start"]
    end = request.get_json()["end"]
    nodeList.set_list(fn.readMaze(map, start, end))
    shortestPath = fn.findShortestPath(nodeList.get_start(), nodeList.get_end())
    return jsonify({"path": shortestPath}), 200


@app.route("/solvePartially", methods=['POST'])
def solvePartially():
    currentPos = request.get_json()["currentPos"]
    shortestPath = fn.findShortestPath(nodeList.get_currentPos(currentPos), nodeList.get_end())
    return jsonify({"path": shortestPath}), 200


if __name__ == '__main__':
    app.run(debug=True)
