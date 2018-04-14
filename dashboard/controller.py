from flask import render_template, jsonify, request
from dashboard import app

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
# Communicate with data model
#
@app.route('/job', methods=['GET','POST'])
def job():
    content = request.get_json()
    #someVariable = content['someVariable']
    print('META recieved:\n', content)
    data = {"PLATSNUMMER": "0017-653836", "ANTAL_AKT_PLATSER": "1",     	"PLATSRUBRIK": "Assistent till Igelboda skola i Saltsj\u00f6baden",     	"YRKE_ID": "5718",     	"VARAKTIGHET": "Tills vidare",     	"ARBETSTID": "Heltid",     	"ARBETSDRIFT": "Dagtid",     	"AG_NAMN": "Nacka kommun, V\u00e4lf\u00e4rd skola, Igelboda skola och f\u00f6rskola",     	"ADRESSLAND": "",     	"POSTORT": "",     	"PLATSBESKRIVNING": "Nackas kommunala skolor n\u00e5r goda resultat tack vare v\u00e5ra fantastiska medarbetare som v\u00e5gar arbeta p\u00e5 nya s\u00e4tt.Genom ny och bepr\u00f6vad pedagogik bejakar vi kreativitet f\u00f6r att stimulera barns och ungdomars l\u00e4rande.Vi har ett aktivt utbyte mellan v\u00e5ra 2 600 medarbetare som arbetar inom f\u00f6rskola, grundskola och gymnasium.P\u00e5 Igelboda skola har vi h\u00f6ga f\u00f6rv\u00e4ntningar och stark gemenskap, d\u00e4r nyt\u00e4nkande och traditioner skapar en l\u00e4randemilj\u00f6 i framkant.Barn, elever och personal har tillsammans skapat v\u00e5r gemensamma v\u00e4rdegrund som \u00e4r utg\u00e5ngspunkt f\u00f6r v\u00e5r starka gemenskap och l\u00e4randemilj\u00f6.P\u00e5 Igelboda skola &amp; f\u00f6rskola ser vi anv\u00e4ndandet av modern teknik som ett naturligt redskap och en m\u00f6jlighet i elevers och barns l\u00e4rsituationer.Vi erbjuder Montessori som pedagogisk inriktning f\u00f6r \u00e5r F-3.Igelboda skola \u00e4r en F-6 skola och f\u00f6rskola samt integrerad fritidsverksamhet.H\u00e4r arbetar idag 70 personer och arbetsplatsen k\u00e4nnetecknas av drivkraft, traditioner, v\u00e4rdegrundsarbete gemenskap.Natursk\u00f6na skolg\u00e5rdar inbjuder till lekfullt l\u00e4rande f\u00f6r v\u00e5ra 500 barn och elever.Skolan ligger centralt vid Saltsj\u00f6badens centrum med n\u00e4rhet till aff\u00e4rer, gratis parkering om du kommer med bil annars bara 20 min fr\u00e5n Slussen med t\u00e5g.Arbetsbeskrivning Assistent till en elev under skoldagen och arbete p\u00e5 fritids under eftermiddagen.Du kommer att vara ett viktigt st\u00f6d n\u00e4r\u00a0eleven beh\u00f6ver det och i bakgrunden n\u00e4r\u00a0du m\u00e4rker att eleven klarar\u00a0sig sj\u00e4lv.Du kommer att ha n\u00e4ra kontakt med elevens v\u00e5rdnadshavare och beh\u00f6ver skapa ett f\u00f6rtroligt samarbete med dem.Till din hj\u00e4lp och handledning har skolan ett elevv\u00e5rdsteam, d\u00e4r psykologen handleder dig och \u00f6vriga av skolans assistenter regelbundet.Ditt f\u00f6rh\u00e5llningss\u00e4tt skall vara samarbetsinriktat, din inst\u00e4llning 'att barn g\u00f6r r\u00e4tt om de kan' och din uppfattning att skola och fritids har ansvar att m\u00f6ta och utveckla varje elev d\u00e4r hen befinner sig socialt och kunskapsm\u00e4ssigt.Vi erbjuder dig Ett sp\u00e4nnande, utmanande och roligt arbete tillsammans med utvecklingsorienterade och engagerade kollegor i skolan och p\u00e5 fritids.Du kommer att f\u00e5 ett eget IT-verktyg, friskv\u00e5rdsbidrag och arbetskl\u00e4der f\u00f6r utomhusbruk.Nacka kommun har ett omfattat fortbildningsprogram att ta del av.Krav f\u00f6r tj\u00e4nsten Du skall ha barnsk\u00f6tarutbildning eller motsvarande utbildning.Erfarenhet av arbete i barngrupp\u00a0och ett stort\u00a0intresse f\u00f6r att arbete med barn i behov av s\u00e4rskilt st\u00f6d.God kommunikationsf\u00f6rm\u00e5ga och flytande svenska i tal och skrift \u00e4r ett krav.Vi l\u00e4gger stor vikt vid personlig l\u00e4mplighet som integritet, samarbetsf\u00f6rm\u00e5ga, flexibilitet, f\u00f6rm\u00e5ga att se och agera efter hela enhetens b\u00e4sta, att kvitta nyttan f\u00f6r andra f\u00f6re sig sj\u00e4lv osv. F\u00f6rh\u00e5llningss\u00e4ttet att alltid utg\u00e5 fr\u00e5n uppdraget \u00e4r v\u00e4sentligt f\u00f6r att lyckas i din roll och f\u00f6r att m\u00e5 bra p\u00e5 jobbet.V\u00e4lkommen med din ans\u00f6kan!Inf\u00f6r rekryteringsarbetet har vi p\u00e5 Nacka kommun tagit st\u00e4llning till rekryteringskanaler och marknadsf\u00f6ring.Vi undanber oss d\u00e4rf\u00f6r best\u00e4mt kontakt med medias\u00e4ljare, rekryteringssajter och liknande.Nacka v\u00e4xer och bygger stad.Vi \u00e4r en \u00f6ppen, enkel och smart kommun som pr\u00e4glas av valfrihet, effektivt resursutnyttjande och dialog med medborgarna.M\u00e5ngfald och \u00f6ppenhet \u00e4r viktiga ledstj\u00e4rnor i kommunen d\u00e4r stadens puls m\u00f6ter hav och skog och d\u00e4r m\u00e4nniskor kan f\u00f6rverkliga sina dr\u00f6mmar.Vi ska vara b\u00e4st p\u00e5 att vara kommun och beh\u00f6ver de b\u00e4sta medarbetarna f\u00f6r att tillsammans uppn\u00e5 den ambitionen.",     	"BESKR_ARBETSDRIFT": " 100 %. Tilltr\u00e4de: 8/1 2018 tillsvidareanst\u00e4llning",     	"TILLTRADE": "",     	"SISTA_ANSOK_PUBLDATUM": "2017-12-15",     	"FORSTA_PUBLICERINGSDATUM": "2017-11-24",     	"KOMMUN_KOD": "0182"     }
    response = jsonify(data)
    #print(response)
    return response
