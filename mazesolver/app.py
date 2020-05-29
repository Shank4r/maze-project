from flask import Flask, jsonify, request
from flask_cors import CORS
from Utilities import functions as fn

app = Flask(__name__)

CORS(app)


@app.route('/getMaze', methods=['POST'])
def getMaze():
    maze = request.get_json()["maze"]
    test = fn.readMaze(maze)
    shortestPath = fn.findShortestPath(test[0], test[1])
    return jsonify({"path": shortestPath}), 200


if __name__ == '__main__':
    app.run(debug=True)

