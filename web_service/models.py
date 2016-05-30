from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ACTIONS = ('NOTIFY', 'BLOCK', 'ACCEPT', 'BLOCK_NOTIFY')
PROTOCOLS = ('tcp', 'udp')
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(512))

    def __repr__(self):
        return '<User {0}>'.format(self.username)

class Rule(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    port = Column(Integer)
    protocol = Column(Enum(*PROTOCOLS))
    action = Column(Enum(*ACTIONS))

    #ordering by the mac id and one to one
    ip = relationship("IP", backref=backref('rules', order_by=id), \
                        uselist=False)

    #ordering by the mac id and one to one
    mac = relationship("MAC", backref=backref('rules', order_by=id), \
                        uselist=False)

    def __repr__(self):
        return '<Rule {0} @ {1} with: {2}'.format(self.protocol, self.port, \
                                                  self.action)

class Packet(Base):
   __tablename__ = 'packets'

   id = Column(Integer(), primary_key=True)
   port = Column(Integer())
   protocol = Column(Enum(*PROTOCOLS))
   date = Column(String(258))
   source = Column(String(124))
   host = Column(String(124))

   def __repr__(self):
       return '<Packet {0}:{1} @ {2}'.format(self.protocol, self.port, self.date)
   # Put the proper Rule that has been violated with an relationship

class IP(Base):
    __tablename__ = 'ips'

    id = Column(Integer(), primary_key=True)
    rule_id = Column(Integer(), ForeignKey("rules.id"), nullable=False)
    ip = Column(String(50))
    ipv4 = Column(Boolean(), default=True)

    def __repr__(self):
        return '<IP id:{0} [{1}] v4? {2} rule:{3}'.format(self.id, self.ip, \
                                                 self.rule_id, self.ipv4)

class MAC(Base):
    __tablename__ = 'macs'

    id = Column(Integer(), primary_key=True)
    rule_id = Column(Integer(), ForeignKey('rules.id'), nullable=False)
    mac = Column(String(50))


    def __repr__(self):
        return '<MAC id: {0} [{1}] rule:{2}'.format(self.id, self.mac, \
                                                    self.rule_id)

def create_db(uri='sqlite:///./heimdall.sqlite3'):
    from sqlalchemy import create_engine
    engine = create_engine(uri)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_session(uri='sqlite:///./heimdall.sqlite3'):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(autocommit=True, autoflush=True, \
                           bind=create_engine(uri))
    return scoped_session(Session)