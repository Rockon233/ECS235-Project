from flask import Flask, request, jsonify, render_template

from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
import time
import logging
from collections import defaultdict

logging.basicConfig(
    filename = 'traffic.log',
    level = logging.INFO,
    format='%(asctime)s - %(message)s',  

)

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://root:password@localhost:3000/classdb?authSource=admin"
mongo = PyMongo(app)

socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin requests for WebSocket
traffic_data = []
traffic_counts = defaultdict(int)

@app.route('/', methods=['GET'])
def hello():
    return "Hello world"

@app.route('/insert', methods=['POST'])
def insert():
    record_traffic(request)  # Track this endpoint
    print(request.json)
    return '', 200


@app.route('/test', methods=['POST'])
def test():
    record_traffic(request)
    try:
        print("Request received in Flask")
        data = request.json
        mongo.db.classdb.insert_one(data)
        return jsonify({"msg": "Document added successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/traffic', methods=['GET'])
def traffic():
    return render_template('traffic.html')

@app.route('/monitor', methods=['GET'])
def monitor():
    return render_template('monitor.html')

def record_traffic(req, success=True):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    traffic_entry = {
        "time": current_time,
        "endpoint": req.path,
        "method": req.method,
        "status": "Success" if success else "Failed",
        "data": req.json or {}
    }
    traffic_data.append(traffic_entry)
    traffic_counts[current_time] += 1
    socketio.emit('traffic_update', traffic_entry)
    socketio.emit('traffic_chart', {"time": current_time, "count": traffic_counts[current_time]})
    log_message = f"Time: {current_time}, Endpoint: {req.path}, Method: {req.method}, " \
                  f"Status: {'Success' if success else 'Failed'}, Data: {req.json or {}}"
    logging.info(log_message)
    
if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)

