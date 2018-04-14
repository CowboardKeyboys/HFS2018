from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/')
def index_page():
    return render_template("index.html")


@app.route('/send_data', methods=['POST'])
def send_data():
    content = request.get_json()
    someVariable = content['someVariable']
    data = {'someVariable': someVariable + " testValue - hackathon"}
    response = jsonify(data)
    print response
    return response


if __name__ == '__main__':
    app.run()
