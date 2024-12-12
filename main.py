from flask import Flask, request, jsonify, render_template, redirect, url_for, session

from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
import time
import logging
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from encryption.aes import AESOBJ
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from bson.json_util import dumps
import json

logging.basicConfig(
    filename = 'traffic.log',
    level = logging.INFO,
    format='%(asctime)s - %(message)s',  
)

key = b'sixteen_byte_key'  # 16-byte key, Byte string
cipher = AES.new(key, AES.MODE_ECB)
# key = b'8bytekey'  # 8-byte key, Byte string
# cipher = AES.new(key, AES.MODE_ECB)
rsaKey = RSA.generate(2048)
private_key = rsaKey.export_key()
public_key = rsaKey.publickey().export_key()


app = Flask(__name__)
app.secret_key = "your_unique_secret_key"

app.config["MONGO_URI"] = "mongodb://root:password@localhost:3000/classdb?authSource=admin"
mongo = PyMongo(app)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin requests for WebSocket
traffic_data = []
traffic_counts = defaultdict(int)

# Middleware for access control
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session or session['role'] != "admin":
            return redirect(url_for('permission_deny'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/index', methods = ["GET"])
def index():
    return redirect(url_for('main'))

@app.route('/admin')
@admin_required
def admin():
    return "Welcome to the Admin Dashboard!!"

@app.route('/permission_deny')
def permission_deny():
    return "Permission Deny! (contact admin)"

@app.route('/signup', methods=['GET'])
def render_signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        role = data.get('role','guest')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check if the user already exists
        if mongo.db.users.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 409

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:600000', salt_length=16)

        mongo.db.users.insert_one({
            "username": username,
            "password": hashed_password,
            "role": role,
            "created_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        })
        
        return jsonify({"msg": "User created successfully!"}), 201
    except Exception as e:
        logging.error(f"Signup error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/insert', methods=['POST'])
def insert():
    record_traffic(request) 
    print(request.json)
    return '', 200


@app.route('/test', methods=['POST'])
def test():
    record_traffic(request)
    try:
        start = time.perf_counter()
        data = request.json
        padded_plaintext = pad(data['word'].encode('utf-8'), 16)  # Pad to match block size
        ciphertext = cipher.encrypt(padded_plaintext)
        document = {"ciphertext": ciphertext}
        mongo.db.classdb.insert_one(document)
        duration = time.perf_counter() - start
        print(f"{duration:.6f}", end=", ")

        # start_dec = time.perf_counter()
        # decipher = AES.new(key, AES.MODE_ECB)
        # deciphertext = unpad(decipher.decrypt(ciphertext), 16)
        # duration_dec = time.perf_counter() - start_dec
        # print(f"Decrypted text: {deciphertext.decode('utf-8')}")
        # print(f"Decryption took {duration_dec:.6f} seconds")

        # document = {
        #     "ciphertext": ciphertext,
        #     "deciphertext": deciphertext.decode('utf-8'),
        #     "encryption_duration": f"{duration:.6f} seconds",
        #     "decryption_duration": f"{duration_dec:.6f} seconds",
        #     }
        # mongo.db.classdb.insert_one(data )
        # duration_dec = time.perf_counter() - start
        # print(f"{duration_dec:.6f}", end=", ")
        
        return jsonify({"msg": "Document added successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/testrsa', methods=['POST'])
def testrsa():
    record_traffic(request)
    try:
        start = time.perf_counter()
        data = request.json
        plaintext = data['word'].encode()
        cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
        ciphertext = cipher.encrypt(plaintext).hex()
        duration = time.perf_counter() - start
        print(f"Encryption duration: {duration:.6f} seconds")

        dec_start = time.perf_counter()
        cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
        decrypted = cipher.decrypt(bytes.fromhex(ciphertext))
        dec_duration = time.perf_counter() - dec_start
        print("Decrypted Plaintext:", decrypted.decode())
        print(f"Decryption duration: {dec_duration:.6f} seconds")

        document = {
            "ciphertext": ciphertext,
            "deciphertext": decrypted.decode('utf-8'),
            "encryption_duration": f"{duration:.6f} seconds",
            "decryption_duration": f"{dec_duration:.6f} seconds",
            }
        mongo.db.classdb.insert_one(document)

        return jsonify({"msg": "Document added successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/getdata', methods=['GET'])
def get_data():
    # record_traffic(request)
    try:
        start = time.perf_counter()
        data = mongo.db.classdb.find()
        data = json.loads(dumps(data))
        duration = time.perf_counter() - start
        print(f"Database read duration: {duration:.6f} seconds")
        return jsonify(data), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/traffic', methods=['GET'])
@login_required
def traffic():
    return render_template('traffic.html')

@app.route('/monitor', methods=['GET'])
@admin_required
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
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Serve the login page

    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Check if the user exists in the database
        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            # Store user session
            session['user'] = username
            session['role'] = user['role']
            # if user['role'] == "admin":
            #     return redirect(url_for('admin'))
            return jsonify({"msg": "Login successful!", "role": user['role']}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True, log_output=True)

