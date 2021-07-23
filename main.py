# main.py

# Import the Flask module that has been installed.

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

import geojson
import shapely.wkt
# pip install dnspython

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://studente:studente@relab.rytr6.mongodb.net/ReLab?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/addresses', methods=['GET'])
def get_all_addresses():
    mil4326WKT = mongo.db.MilWKT4326
    output = []
    for s in mil4326WKT.find().limit(100):
        output.append(s['INDIRIZZO'] + "|" + s['CI_VETTORE'])
    return jsonify({'result': output})

# Estrae consumo energetico medio e totale raggruppato per sezione catastale (e Poligono WKT)
@app.route('/avgs', methods=['GET'])
def get_all_stars():
    mil4326WKT = mongo.db.MilWKT4326
    output = []

    match = {
        '$match': {
            'EP_H_ND': {
                '$gt': 0
            }
        }
    }
    group = {
        '$group': {
            '_id': {
                'SEZ': '$SEZ',
                'WKT': '$WKT'
            },
            'AVG': {
                '$avg': '$EP_H_ND'
            },
            'SUM': {
                '$sum': '$EP_H_ND'
            }
        }
    }
    limit = {
        '$limit' : 10
    }
    
    for s in mil4326WKT.aggregate([match, group, limit]):
        g1= shapely.wkt.loads(s['_id']['WKT']) #Converte da WKT in GeoJson Geometry
        g2 = geojson.Feature(geometry=g1, 
        properties={'id':s['_id']['SEZ'], 'media':s['AVG'], 'somma':s['SUM'], 'sezione':s['_id']['SEZ']}) 
        output.append(g2)                 
    return jsonify({'result': output})


# Annotation that allows the function to be hit at the specific URL.
@app.route("/")
# Generic Python functino that returns "Hello world!"
def index():
    return "Hello world!"

# Checks to see if the name of the package is the run as the main package.
if __name__ == "__main__":
    # Runs the Flask application only if the main.py file is being run.
    app.run()
