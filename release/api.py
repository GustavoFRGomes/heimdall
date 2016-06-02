from flask import Flask
from flask.ext.restful import Api
from flask.ext.httpauth import HTTPAuth # Check if it's this the name

app = Flask(__name__)
api = Api(app)

# importing the Resources to handle the HTTP requests
from api_resources import RuleResource
from api_resources import CounterResource
from api_resources import RuleListResource
from api_resources import CounterListResource

"""
API description and mapping:
    Rule receives an ID and is used in GET, DELETE and PUT requests.
    ListRules lists the rules with a GET, appends rules with POST
    Counter receives an ID and only uses GET to display a counter for one rule
    ListCounters lists all the counters with a GET.
"""

api.add_resource(RuleResource, '/rule/<int:id>') # check what the endpoint is for.
api.add_resource(CounterResource, '/counter/<int:id>')
api.add_resource(RuleListResource, '/rules')
api.add_resource(CounterListResource, '/counters')

if __name__ == '__main__':
    context = ('tls/heimdall.crt', 'tls/heimdall.key')
    app.run(debug=True, ssl_context=context)
