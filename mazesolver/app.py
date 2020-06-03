from flask import Flask, jsonify, request
from flask_cors import CORS
from Utilities import functions as fn

app = Flask(__name__)

CORS(app)


@app.route('/getMaze', methods=['POST'])
def getMaze():
    map = request.get_json()["map"]
    start = request.get_json()["start"]
    end = request.get_json()["end"]
    test = fn.readMaze(map, start, end)
    shortestPath = fn.findShortestPath(test[0], test[1])
    return jsonify({"path": shortestPath}), 200


if __name__ == '__main__':
    app.run(debug=True)

