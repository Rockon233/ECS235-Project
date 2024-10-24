from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello world"


@app.route('/insert', methods=['POST'])
def insert():
    print(request.json)
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)

