from flask import Flask, request, jsonify, render_template

from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:3000/classdb"
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def hello():
    return "Hello world"

@app.route('/insert', methods=['POST'])
def insert():
    print(request.json)
    return '', 200

@app.route('/test', methods=['POST'])
def test():
    print("Request recieved in Flask")
    data = request.json
    mongo.db.classdb.insert_one(data)
    return jsonify({"msg": "Document added successfully!"}), 201


if __name__ == '__main__':
    app.run(port = 8000, debug=True)

