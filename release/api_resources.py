from models import Rule, IP, MAC
from models import User
from models import Counter
from models import create_session

from flask import request
from flask.ext.httpauth import HTTPBasicAuth as httpauth
from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from flask.ext.restful import Resource

from sqlalchemy.exc import IntegrityError, InvalidRequestError
from time_aux import getTime # create a timestamp getter returns string

ip_fields = {
        'ip': fields.String,
        'ipv4': fields.Boolean,
}

mac_fields = {
        'mac': fields.String,
}

rule_fields = {
        'id': fields.Integer,
        'port': fields.String,
        'protocol': fields.String,
        'action': fields.String,
        'ip': ip_fields,
        'mac': mac_fields,
}

counter_fields = {
        'id': fields.Integer,
        'packets': fields.Integer,
        'byte': fields.Integer,
}

# rules_fields = {
#         'rules': fields.List(fields.Nested(rule_fields)),
# }

counters_fields = {
        'counters': fields.List,
}

# Creating a common session for the Database.
session = create_session()
auth = httpauth()

# @auth.get_password
# def get_pwd(username):
#     user = session.query(User).filter(username == User.username).first()
#     print(user)
#     if user:
#         return user.password # send password
#     return None

@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter(username==User.username).first()
    if not user or not user.check_password(password):
        # abort(401, message="Username and/or Password wrong!")
        return False
    session.begin()
    user.timestamp = getTime()
    try:
        session.commit()
    except (InvalidRequestError, IntegrityError) as e:
        print('Problem adding timstamp to user login.')
        session.rollback()

    return True

class RuleResource(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('port')
        self.reqparser.add_argument('protocol')
        self.reqparser.add_argument('action')
        self.reqparser.add_argument('ip')
        self.reqparser.add_argument('mac')
        super(RuleResource, self).__init__()

    @marshal_with(rule_fields)
    def get(self, id):
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in the DB.".format(id))
        return rule

    def delete(self, id):
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in the DB.".format(id))
        session.begin()
        session.delete(rule)
        session.commit()
        # return 'Removed Successful', 200

    def put(self, id):
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in the DB.".format(id))
        # args = self.reqparser.parse_args()
        args = request.get_json(force=True)
        rule.protocol = args['protocol']
        rule.port = args['port']
        rule.action = args['action']

        ip = args.get('ip', None)
        mac = args.get('mac', None)

        # Check if ip and mac is passed and created by these things.
        if ip:
            rule.ip = IP(ip['ip'], ip['ipv4'])
        if mac:
            rule.mac = MAC(mac['mac'])

        # session.add(rule)
        session.commit()
        # return 'Edit Successful', 200

class CounterResource(Resource):
    # def __init(self):
    #     self.reqparser = reqparse.RequestRarser()
    #     self.reqparser.add_argument('packets')
    #     self.reqparser.add_argument('byte')
    #     super(CounterResource, self).__init__()
    decorators = [auth.login_required]

    @marshal_with(counter_fields)
    def get(self, id):
        counter = session.query(Counter).filter(Counter.id == id).first()
        if not counter:
            abort(404, message="Can't find {0} in the DB.".format(id))
        return counter

class CounterListResource(Resource):
    decorators = [auth.login_required]
    @marshal_with(counters_fields)
    def get(self):
        counters = session.query(Counter).all()
        return counters

class RuleListResource(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('port', dest='port')
        self.reqparser.add_argument('protocol', dest='protocol')
        self.reqparser.add_argument('action', dest='action')
        self.reqparser.add_argument('ip', dest='ip')
        self.reqparser.add_argument('mac', dest='mac')
        super(RuleListResource, self).__init__()

    @marshal_with(rule_fields)
    def get(self):
        rules = session.query(Rule).all()
        # print(rules)
        return rules

    def post(self):
        # args = self.reqparser.parse_args()
        args = request.get_json(force=True)
        rule = Rule()
        rule.protocol = args['protocol']
        rule.port = str(args['port'])
        rule.action = args['action']

        ip = args.get('ip', None)
        mac = args.get('mac', None)

        # Check if ip and mac is passed and created by these things.
        if ip:
            new_ip = IP()
            new_ip.ip = ip['ip']
            new_ip.ipv4 = ip['ipv4']
            rule.ip = new_ip
        if mac:
            rule.mac = MAC()
            rule.mac.mac = mac['mac']

        session.begin()
        session.add(rule)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return "Unable to insert that rule, check passed params", 500


