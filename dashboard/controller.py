from flask import render_template, jsonify, request, Response
from dashboard import app

# import models
from dashboard.static.data.database import database
db = database(source='dashboard/static/data/200.json')

#
# Render views
#

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Customer portal')

@app.route('/register')
def register():
    client_id = '31u412h9p45rt3faf'
    return render_template('register.html', title='Register customer', customer=client_id)

#
# Request NLP processing
#
@app.route('/process_resume', methods=['GET','POST'])
def get_score_from_text():
    data = "TEXT"
    hampus_result = data
    jocktor_result = {'id': 1, 'regions':[]}
    response = jsonify(data)
    return response

#
# Score by region based on applicable jobs
#

#
# Communicate with data model and list job posting
#
@app.route('/job', methods=['POST'])
def job():
    content = request.get_json()
    id = content['job_id']
    posting = db.get_job_from_id(id)
    return Response(posting,status=200)
