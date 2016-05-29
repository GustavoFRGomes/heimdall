from models import Rule, User, Packet, IP, MAC
from models import create_db, create_session

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with

packet_fields = {
    'id': fields.Integer,
    'date': fields.String,
    'protocol': fields.String,
    'port': fields.Integer,
    'source': fields.String,
    'host': fields.String,
}
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
}

rule_fields = {
    'id': fields.Integer,
    'port': fields.Integer,
    'protocol': fields.String,
    'action': fields.String,
}

session = create_session()

#parser = reqparse.RequestParser()
#parser.add_argument('id')
#parser.add_argument('username')
#parser.add_argument('')

class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        #self.reqparse.add_argument('id')
        self.reqparse.add_argument('username')
        self.reqparse.add_argument('password')
        super(UserResource, self).__init__()

    @marshal_with(user_fields)
    def get(selfself, id):
        user = session.query(User).filter(User.id==id).first()
        if not user:
            abort(404, message="Can't find {0} in User Table".format(id))
        return user
    def delete(self, id):
        user = session.query(User).filter(User.id==id).first()
        if not user:
            abort(404, message="Can't find {0} in User Table".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = self.reqparse.parse_args()
        user = session.query(User).filter(User.id == id).first()
        # check if user exists or not
        user.username = parsed_args['username']
        user.password = parsed_args['password']
        session.add(user)
        session.commit()
        return user, 201

    @marshal_with(user_fields)
    def post(self):
        parsed_args = self.reqparse.parse_args()
        user = User(username=parsed_args['username'], \
                    password=parsed_args['password'])
        session.add(user)
        session.commit()
        return user, 201

class RuleResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        #self.reqparse.add_argument('id')
        self.reqparse.add_argument('port')
        self.reqparse.add_argument('protocol')
        self.reqparse.add_argument('action')
        super(RuleResource, self).__init__()

    @marshal_with(rule_fields)
    def get(self, id):
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in Rule Table".format(id))
        return rule
    # put
    @marshal_with(rule_fields)
    def put(self, id):
        parsed_args = self.reqparse.parse_args()
        rule = session.query(Rule).filter(Rule.id == id).first()
        # check if user exists or not
        rule.protocol = parsed_args['protocol']
        rule.port = parsed_args['port']
        rule.action = parsed_args['action']
        session.add(rule)
        session.commit()
        return rule, 201

    def delete(self, id):
        rule = session.query(Rule).filter(Rule.id == id).first()
        if not rule:
            abort(404, message="Can't find {0} in Rule Table".format(id))
        session.delete(rule)
        session.commit()
    # delete
    # post
    def post(self):
        parsed_args = self.reqparse.parse_args()
        rule = Rule( port=parsed_args['port'], action=parsed_args['action'], \
                     protocol=parsed_args['protocol'])
        session.add(rule)
        session.commit()
        return rule, 201

class RuleListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        #self.reqparse.add_argument('id')
        self.reqparse.add_argument('port')
        self.reqparse.add_argument('protocol')
        self.reqparse.add_argument('action')
        self.reqparse.add_argument('ip')
        self.reqparse.add_argument('mac')
        super(RuleListResource, self).__init__()

    @marshal_with(rule_fields)
    def get(self):
        return session.query(Rule).all()

    def post(self):
        """
        POST handler to add a new rule to the ruleset.
        :return: empty list with 200 success code tuple.
        """
        args = self.reqparse.parse_args()
        # check for the rule things
        rule = Rule(port=args['port'], protocol=args['protocol'], \
                    action=args['action'])
        ip = args.get('ip', None)
        mac = args.get('mac', None)
        if not (ip == None):
            rule.ip = IP(ip=ip.ip, ipv4=ip.ipv4)
        if not (mac == None):
            rule.mac = MAC(mac=mac.mac)

        session.add(rule)
        session.commit()
        return [], 200

class PacketListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        #self.reqparse.add_argument('id')
        self.reqparse.add_argument('port')
        self.reqparse.add_argument('protocol')
        self.reqparse.add_argument('date')
        self.reqparse.add_argument()
        super(PacketListResource, self).__init__()

    # only needs a packet getter
    @marshal_with(packet_fields)
    def get(self):
        packet = session.query(Packet).all()
        # send an empty packet list to signal that it is empty
        return packet

