from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)
api = Api(app)

from resources import RuleResource
from resources import UserResource
from resources import RuleListResource
from resources import PacketListResource

api.add_resource(UserResource, '/users/<int:id>', endpoint='user')
api.add_resource(RuleResource, '/rule/<int:id>', endpoint='rule')
api.add_resource(RuleListResource, '/rules', endpoint='rules')
api.add_resource(PacketListResource, '/packets', endpoint='packets')

# Need Resources for listing all not just one in specific.
if __name__ == '__main__':
    app.run(debug=True)