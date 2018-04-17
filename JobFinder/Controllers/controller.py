#-*-coding: utf-8-*-
from flask import render_template, jsonify, request, Response, redirect
from JobFinder import app
from JobFinder.Models.municipal_weighting import *
import json
# import models
from JobFinder.Models.database import Database
from JobFinder.Models.nlp_calculator import NLPCalculator

db = Database(source='JobFinder/Assets/200.json')
nlp = NLPCalculator(db.get_jobs())
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
# Communicate with data Models and list job posting
#
@app.route('/job', methods=['POST', 'GET'])
def job():
    content = request.get_json()
    id = content['job_id']
    job = db.get_job_from_id(id)
    #h = Headers()
    #h.add('Access-Control-Allow-Origin','*')
    response = Response(json.dumps(job),status=200)#, headers=h)
    return response

@app.route('/jobs', methods=['POST'])
def jobs_by_id():
    content = request.get_json()
    ids = content['job_id']
    jobs = db.get_job_from_id(ids)
    response = Response(json.dumps(jobs),status=200)
    return response

# Returns all jobs in the databse.
@app.route('/jobs', methods=['GET'])
def jobs():
    jobs = db.get_all_jobs().encode('utf8')
    response = Response(jobs, status=200)
    return response

@app.route('/jobs/region', methods=['POST'])
def jobs_by_region():
    content = request.get_json()
    region = content['region']
    jobs = db.get_jobs_in_region(region_code=region)
    response = Response(json.dumps(jobs), status=200)
    return response

@app.route('/match', methods=['POST', 'GET'])
def match_with_listings():
    if request.method == 'POST':
        result = request.form
        result = nlp.match_text(result['curriculum'], 10)
        municipals = get_region_score(result)
        data = {'municipals': municipals}
        return render_template('regions.html', title='Results', regions=data['municipals'])
    else:
        return redirect('/')
