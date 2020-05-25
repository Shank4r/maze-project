from flask import Flask, jsonify, request
from flask_cors import CORS
from Utilities import functions as fn

app = Flask(__name__)

CORS(app)


@app.route('/getMaze', methods=['POST'])
def getMaze():
    maze = request.get_json()["maze"]
    fn.readMaze(maze)
    return jsonify({"message": "hei verden"}), 200


if __name__ == '__main__':
    app.run(debug=True)

