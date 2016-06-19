from models import Rule, IP, MAC
from models import User
from models import Counter
from models import create_session

from flask import request
from flask_httpauth import HTTPBasicAuth as httpauth
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import Resource

from validate import validIpv4, validMac

from sqlalchemy.exc import IntegrityError, InvalidRequestError
from time_aux import getTime # create a timestamp getter returns string

import json

ip_fields = {
        'ip': fields.String,
        'ipv4': fields.Boolean,
        'src': fields.Boolean,
}

mac_fields = {
        'mac': fields.String,
}

rule_fields = {
        'id': fields.Integer,
        'port': fields.String,
        'protocol': fields.String,
        'action': fields.String,
        'ip': fields.Nested(ip_fields),
        'mac': fields.Nested(mac_fields),
}

counter_fields = {
        'rule_id':fields.Integer,
        'id': fields.Integer,
        'packets': fields.Integer,
        'byte': fields.Integer,
}

# rules_fields = {
#         'rules': fields.List(fields.Nested(rule_fields)),
# }

# counters_fields = {
#         'counters': fields.List,
# }

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

        self.session = create_session()

        super(RuleResource, self).__init__()

    @marshal_with(rule_fields)
    def get(self, id):
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in the DB.".format(id))
        return rule

    def delete(self, id):
        print('DELETE Called!')
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in the DB.".format(id))
        session.begin()
        print(rule.ip)
        print(rule.mac)
        if not (rule.ip == None):
            session.delete(rule.ip)
        if not (rule.mac == None):
            session.delete(rule.mac)
        session.delete(rule)
        session.commit()
        # return 'Removed Successful', 200

    def put(self, id):
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in the DB.".format(id))
        # args = self.reqparser.parse_args()
        args = request.get_json(force=True)
        print(args)
        # print(json.loads(args))
        if(type(args) == type("")):
            args = json.loads(args)
        # print(args.keys())
        setattr(rule, 'protocol', args['protocol'])
        setattr(rule, 'port', args['port'])
        setattr(rule, 'action', args['action'])

        ip = args.get('ip', None)
        mac = args.get('mac', None)
        # Check if ip and mac is passed and created by these things.
        if ip:
            if not validIpv4(ip['ip']):
                abort(401, message='Invalid IPv4 address!')
            setattr(rule, 'ip', IP(ip=ip['ip'], ipv4=ip['ipv4'], src=ip['src']))
        if mac:
            if not validMac(mac['mac']):
                abort(401, message='Invalid MAC address!')
            setattr(rule, 'mac', MAC(mac=mac['mac']))
            # rule.mac = MAC(mac=mac['mac'])
        # session.add(rule)
        try:
            session.commit()
        except:
            session.rollback()
            print("Rollback needed")
            return "Unable to insert that rule, check passed params", 500


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
        counter = session.query(Counter).filter(Counter.rule_id == id).all()
        if not counter:
            abort(404, message="Can't find {0} in the DB.".format(id))
        if type(counter) == type([]):
            return counter
        return [counter]

class CounterListResource(Resource):
    decorators = [auth.login_required]
    @marshal_with(counter_fields)
    def get(self):
        size_rules = len(session.query(Rule).all())
        counters = session.query(Counter).all()
        results = counters[(size_rules*(-1)):]
        if type(results) == type([]):
            return results
        return [results]

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

        print(args)

        rule = Rule()
        rule.protocol = args['protocol']
        rule.port = str(args['port'])
        rule.action = args['action']

        ip = args.get('ip', None)
        mac = args.get('mac', None)

        # Check if ip and mac is passed and created by these things.
        if ip:
            if not validIpv4(ip['ip']):
                abort(401, message='Invalid IPv4 address!')
            new_ip = IP()
            new_ip.ip = ip['ip']
            new_ip.ipv4 = ip['ipv4']
            new_ip.src = ip['src']
            new_ip.rule_id = rule.id
            print(new_ip)
            print(rule)
            rule.ip = new_ip
        if mac:
            if not validMac(mac['mac']):
                abort(401, message='Invalid MAC address!')
            rule.mac = MAC()
            rule.mac.mac = mac['mac']


        session.begin()
        session.add(rule)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Rollback needed")
            return "Unable to insert that rule, check passed params", 500


