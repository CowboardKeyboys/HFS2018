#-*-coding: utf-8-*-
from flask import render_template, jsonify, request, Response, redirect, url_for
from dashboard import app
from dashboard.MunicipalWeighting import *
import json
# import models
from dashboard.static.data.database import database
db = database(source='dashboard/static/data/200.json')
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
    response = Response(jobs,status=200)
    return response

@app.route('/match', methods=['POST', 'GET'])
def match_with_listings():
    if request.method == 'POST':
        #content = request.form
        # (ids, scores) = CALL HAMPUS(cv)
        text = "hejsan pizza hamburgare rullstol."
        result = nlp.match_text(text, 20)
        print result
        joktor = []
        for id, score in zip(result["id"],result["score"]):
            job = db.get_job_from_id(id)
            obj = json.loads(job)
            region_code = int(obj['region_code'])
            description = obj['location_desc']
            #print region_code
            joktor.append({'region_code':region_code,'score': score, 'desc':description })
        print joktor
        # regions = CALL JOCKTOR(scored_stuffs)
        data0 = {'region_code': 1440, 'score': 0.1}
        data1 = {'region_code': 1440, 'score': 0.3}
        data2 = {'region_code': 1440, 'score': 0.2}
        data3 = {'region_code': 1489, 'score': 0.4}
        our_list=[data0, data1,data2,data3]
        municipals = get_region_score(joktor)
#        municipals = [{'id':'0', 'name':'South', 'postings': ['0017-653836', '0017-653837']},{'id':'1', 'name':'West', 'postings': ['0017-653842', '0017-653844', '0017-571999', '0017-544195']},{'id':'2', 'name':'East', 'postings': ['0017-681758', '0017-681782']},{'id':'3', 'name':'North', 'postings': ['0017-681757']}]
        data = {'municipals': municipals}
        return render_template('regions.html', title='Results', regions=data['municipals'])
    else:
        return redirect('/')
