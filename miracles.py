from calendar import c
from itertools import count
from flask import Flask, Response, render_template, request, jsonify, url_for
import sqlite3


app = Flask(__name__)

def getCountryMiracles(miracles):
    countries = {}
    for miracle in miracles:
        if miracle[2] not in countries:
            countries[miracle[2]] = {   "total": 1,
                                        "miracles":[{'url':miracle[0], 
                                                    'date':miracle[1],
                                                    'city':miracle[3]
                                                    }]
                                    }                       
        else:
            countries[miracle[2]]['total'] += 1
            countries[miracle[2]]["miracles"].append({  'url':miracle[0], 
                                            'date':miracle[1],
                                            'city':miracle[3]})
    countries['totalCountries'] = len(countries.keys())
    countries['totalMiracles'] = len(miracles)

    return countries

def getSaintMiracles(miracles):
    data = {"miracles": []}
    for miracle in miracles:
        data["miracles"].append({ 'url':miracle[0], 
                                        'saint':miracle[1],
                                        'date':miracle[2]})
    data["totalSaintMiracles"] = len(miracles)
    return data

def getMarianMiracles(miracles):
    data = {"miracles": []}
    for miracle in miracles:
        data["miracles"].append({'url':miracle[0], 
                                        'date':miracle[1],
                                        'country':miracle[2],
                                        'city':miracle[3],
                                        'name':miracle[4]})
    data['totalMarianMiracles'] = len(miracles)
    return data

def getCommunionMiracles(miracles):
    data = {"miracles": []}
    for miracle in miracles:
        data["miracles"].append({ 'url':miracle[0], 
                                            'name':miracle[1]})

    data['totalCommunionMiracles'] = len(miracles)
    return data


@app.route('/', methods=["GET"])
def index():
    return jsonify({"welcome": {
        "msg" : "Thanks for using the Eucharistic Miracles API!",
        "exhibition": "http://www.miracolieucaristici.org",
        "documentation": "https://rapidapi.com/teckneck1.1/api/eucharistic-miracles/",
        "endpoints": ["/all", "/saints", "/countries", "/marian", "/communions"]
        }
    })

@app.route('/all', methods=["GET"])
def all():
    con = sqlite3.connect('miracles.db')
    cur = con.cursor()
    data = {}

    countries = cur.execute('SELECT * FROM countryMiracles').fetchall()
    marian = cur.execute('SELECT * FROM marianMiracles').fetchall()
    communions = cur.execute('SELECT * FROM communionMiracles').fetchall()
    saints = cur.execute('SELECT * FROM saintMiracles').fetchall()

    data["Country Miracles"] = getCountryMiracles(countries)
    data["Marian Miracles"] = getMarianMiracles(marian)
    data["Saint Miracles"] = getSaintMiracles(saints)
    data["Communion Miracles"] = getCommunionMiracles(communions)

    return jsonify(data),200

@app.route('/countries', methods=["GET"])
def countries():
    con = sqlite3.connect('miracles.db')
    cur = con.cursor()
    if request.args.get('country'):
        country = request.args.get('country')
        cur.execute(f'SELECT * FROM countryMiracles WHERE country == (?)',(country,))
    else:
        cur.execute('SELECT * FROM countryMiracles')

    miracles = cur.fetchall()
    if miracles == []:
        return jsonify({"Uh-Oh":"No valid results"}),400

    data = getCountryMiracles(miracles)
    return jsonify(data), 201

@app.route('/saints', methods=["GET"])
def saints():
    con = sqlite3.connect('miracles.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM saintMiracles')
    miracles = cur.fetchall()
    data = getSaintMiracles(miracles)
    return jsonify(data), 201

@app.route('/marian', methods=["GET"])
def marian():
    con = sqlite3.connect('miracles.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM marianMiracles')
    miracles = cur.fetchall()
    data = getMarianMiracles(miracles)
    return jsonify(data), 201


@app.route('/communions', methods=["GET"])
def communions():
    con = sqlite3.connect('miracles.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM communionMiracles')
    miracles = cur.fetchall()
    data = getCommunionMiracles(miracles)
    return jsonify(data), 201

if __name__=='__main__':
    app.run(debug=True)