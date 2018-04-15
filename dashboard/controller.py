#-*-coding: utf-8-*-
from flask import render_template, jsonify, request, Response, redirect, url_for
from dashboard import app
from dashboard.MunicipalWeighting import *
import json
# import models
from dashboard.static.data.database import database
db = database(source='dashboard/static/data/10k.json')
from dashboard.model.nlp.NLPcalculator import NLPcalculator
nlp = NLPcalculator(db.get_training_data())
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
@app.route('/job', methods=['POST', 'GET'])
def job():
    content = request.get_json()
    id = content['job_id']
    job = db.get_job_from_id(id)
    #h = Headers()
    #h.add('Access-Control-Allow-Origin','*')
    response = Response(job,status=200)#, headers=h)
    return response

@app.route('/jobs', methods=['POST'])
def jobs_by_id():
    content = request.get_json()
    ids = content['job_id']
    jobs = db.get_job_from_id(ids)
    response = Response(jobs,status=200)
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
    response = Response(jobs, status=200)
    return response

@app.route('/match', methods=['POST', 'GET'])
def match_with_listings():
    if request.method == 'POST':
        result = request.form
        result = nlp.match_text(result['curriculum'], 10)
        joktor = []
        for id, score in zip(result["id"],result["score"]):
            job = db.get_job_from_id(id)
            obj = json.loads(job)
            try:
                region_code = int(obj['region_code'])
            except ValueError as e:
                region_code = 1440
            description = obj['location_desc']
            joktor.append({'region_code':region_code,'score': score, 'desc':description, 'title': obj['title'] })
        municipals = get_region_score(joktor)
        data = {'municipals': municipals}
        return render_template('regions.html', title='Results', regions=data['municipals'])
    else:
        return redirect('/')
