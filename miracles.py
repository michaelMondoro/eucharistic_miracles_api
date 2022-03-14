from itertools import count
from flask import Flask, Response, request, jsonify
import sqlite3

app = Flask(__name__)

def getCountryMiracles(miracles):
    countries = {}
    for miracle in miracles:
        if miracle[2] not in countries:
            countries[miracle[2]] = [{   'url':miracle[0], 
                                        'date':miracle[1],
                                        'city':miracle[3]}]
        else:
            countries[miracle[2]].append({  'url':miracle[0], 
                                            'date':miracle[1],
                                            'city':miracle[3]})
    return countries

def getSaintMiracles(miracles):
    data = []
    for miracle in miracles:
        data.append({   'url':miracle[0], 
                        'saint':miracle[1],
                        'date':miracle[2]})
    return data

def getMarianMiracles(miracles):
    data = []
    for miracle in miracles:
        data.append({   'url':miracle[0], 
                        'date':miracle[1],
                        'country':miracle[2],
                        'city':miracle[3],
                        'name':miracle[4]})
    return data

def getCommunionMiracles(miracles):
    data = []
    for miracle in miracles:
        data.append({   'url':miracle[0], 
                        'name':miracle[1]})
    return data


@app.route('/', methods=["GET"])
def index():
    return "WELCOME"

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
        return jsonify({"ERROR":"No valid results"}),400

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