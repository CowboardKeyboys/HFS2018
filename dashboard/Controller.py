from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


# TODO - Daniel
# Presents the GUI
@app.route('/')
def index_page():
    return render_template("index.html")


# TODO - Christian
# get job description from id
# input: id
# output: job (object)
@app.route('/get_job_from_id')
def get_job_from_id():
    pass


# TODO - Christian
#  get a list of jobs in a region
# input: list of ids
# output: list of jobs (objects)
@app.route('/get_jobs_in_region')
def get_jobs_in_region():
    pass


# TODO - Hampus
#  match text to score
# input: id, return_object_count
# output: score
@app.route('/get_score_from_text')
def get_score_from_text():
    pass


# TODO - Viktor och Jocke
# input: list of ids
# output: list of jobs (objects)
@app.route('/get_municipal_score')
def get_municipal_score():
    pass


# Example response for a rest API/RESTful
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
