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
        print(result)
        # TODO: AJAX text please!
        #text = "Hej!  När jag läste er annons om tjänsten som sekreterare, som jag fick skickat till mig av en vän idag, så tyckte jag direkt att jobbet verkade vara mycket varierande och roligt och jag tror att jag skulle passa in väldigt bra. Därför skickar jag er min ansökan.  Jag är en mycket noggrann och ansvarsfull kvinna med en hög arbetsmoral. Är glad och positiv och gör alltid mitt bästa. Jag arbetar gärna självständigt, likväl som tillsammans med andra. Har lätt för- och tycker att det är roligt och utmanande att försöka att lära mig nya saker och utvecklas som person.   Jag tycker att den sociala miljön på arbetsplatsen är viktig och jag försöker att bidra till att hålla den positiv genom att vara en bra medarbetare.  Fritiden spenderar jag mestadels med familjen, som består av mig själv, min man och våra två barn som är 10 och 17 år gamla. Jag tränar flera gånger i veckan på gym, vilket jag tycker är väldigt roligt och givande på många sätt.   Som ni ser i mitt CV så har jag arbetat på IKEA de senaste tio åren. Jag har trivts bra men har känt de senare åren att jag gärna vill byta arbetsuppgifter och finnas i en mer social miljö där jag träffar mer.   Jag är fortfarande anställd på XXXXX, men eftersom jag inte har några arbetsuppgifter där längre så har jag möjlighet att börja hos er omedelbart om så skulle behövas. Jag har även en möjlighet att kunna provjobba (eller praktisera kanske det ska kallas) hos er en eller ett par veckor före den 1/12-09, vilket kan vara bra för både er och mig.  Då jag har lite svårt att beskriva mig själv på ett rättvisande sätt, så hoppas jag att vi snart kan ses personligen istället så att ni kan göra er en egen bild av mig som person.  Men vänlig hälsning"
        #text2 = "Hej Accigo! Min passion är och teknik och som både IT & ekonomi så försöker jag alltid ha en helhetssyn på allting jag gör.Jag drivs av mina intressen för både IT & Ekonomi och därför söker jag utmaningar som kombinerar båda ämnena, såsom business intelligence. För närvarande tycker jag cloud computingärspännande och har arbetat med en forskargrupp vid Uppsala universitet för att utveckla en distribuerad molnlösning för en vetenskaplig fysikapplikationochhar även arbetatsom lärarassistent för en kurs inom cloud computing. Min förkärlek till programmering har gjort att jag känner mig som en trygg programmerare och sätter min lätt in i nya programmeringsspråk,men är alltid på jakt efter något att utmana mig ytterligare. Under mina år på universitet harjag varit engageradi olika typer av aktiviteter såsom att organisera ett LAN-party, spelat i ett amerikansk inomhusfotbollslag, arbetat som labbassistent i en fortsättningskurs inom programmering, för den lokala kommunen, och nu även som ordförare i vår alumniförening. Som komplement till att ta del i aktiviteter så studerade jag också under ett par årmed en studietaktpå 150% för att utöka min verktygslåda med företagsekonomi A, Boch Cför att utveckla ett mer affärsanalytiskt perspektivatt komplettera min IT kompetens. Nyligen har jag funnit ämnensom affärsutveckling och värdeskapande för väckt mina intressensom ett resultat av min specialisering. Min inriktning är ett program som organiseras inom alla tekniska och natur naturvetare, där eleverna handplockade för att studera affärsutveckling och relaterade ämnen som en del av sista åretpå civilingenjörsstudierna. Jag har haft mycket roligt att studera, arbeta och ta del i aktiviteterhär vid Uppsala universitet och jag hoppas att i framtiden hitta en arbetsplats där jag kan utmana mig själv, tillämpakreativ problemlösning och arbeta med intressanta och entusiastiska.Varför Accigo?Jag tror att på Accigo finns en entreprenörsanda som skulle passa mig. Min bakgrund inom både och ekonomi så känns det naturligtattarbete med de tjänster ni erbjuder och jag kan förhoppningsvis flersidiga perspektiv i att driva digitalisering, utveckling och andra tjänster.  Som konsult så hoppas jag på att få ta del av förändringsarbete i olika former och göra skillnadför kunder och andra intressenter. Bästa hälsningar, Max Andersson"
        #text2 = "Gillar att jobba med händerna. Tycker om materialet trä. Kan tänkte mig att snickra lite, har en kniv hemma. xbox, ps4, nintendo"
        text2 = 'jag tycker om människor i harmoni. vi lever för utveckling. som utvecklingsingenjör söker jag utmaningar.'
        text5 = 'ekonomi aktier fonder portfölj bank pengar baby money money förvaltningsavgift ips pension isk'
        result = nlp.match_text(result['curriculum'], 10)
        print result
        joktor = []
        for id, score in zip(result["id"],result["score"]):
            job = db.get_job_from_id(id)
            obj = json.loads(job)
            try:
                region_code = int(obj['region_code'])
            except ValueError as e:
                region_code = 1440
            description = obj['location_desc']
            #print region_code
            joktor.append({'region_code':region_code,'score': score, 'desc':description, 'title': obj['title'] })
        municipals = get_region_score(joktor)
        data = {'municipals': municipals}
        return render_template('regions.html', title='Results', regions=data['municipals'])
    else:
        return redirect('/')
