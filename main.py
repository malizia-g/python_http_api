# main.py

# Import the Flask module that has been installed.

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
# pip install dnspython

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://studente:studente@relab.rytr6.mongodb.net/ReLab?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/addresses', methods=['GET'])
def get_all_addresses():
    mil4326WKT = mongo.db.Mil4326WKT
    output = []
    for s in mil4326WKT.find():
        output.append(s['INDIRIZZO'])
    return jsonify({'result': output})


@app.route('/avgs', methods=['GET'])
def get_all_stars():
    mil4326WKT = mongo.db.Mil4326WKT
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

    for s in mil4326WKT.aggregate([match, group]):
        output.append({'somma': s['SUM'], 'media': s['AVG'],
                      'WKT': s['_id']['WKT'], 'SEZ': s['_id']['SEZ']})
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
