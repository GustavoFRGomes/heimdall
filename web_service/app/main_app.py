from flask import Flask, request
from flask_return import Resource, Api

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

class DatabaseHandler():
    def __init__(self, db_name='heimdall_db', port=27017):
        self.db = MongoClient('mongodb://'+db_name+':'+str(port))

class Authenticate(Resource):
    def verify_token(self, token):
        pass

class Rules(Resource):
    def get_rules(self):
        return []
    def add_rule(self, rule):
        # Add a rule to the database
        return True

class Api(Resource):
    def get_packet():
        pass

class WebService(Resource):
    def __init__(self):
        # Connect to the DB
        # Make the Users attribute with the DBs resources
        # Get the rules of the System
        # Make the resource up and running.
        # Tests and initialize the token seed
        pass

# Make more resources
api.add_resource(Authenticate, '/<string:authenticate>')

if __name__ == '__main__':
    app.run(debug=True)
