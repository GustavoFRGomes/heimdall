import sys
from pymongo import Connection
from pymongo import ConnectionFailure

class DBHandler():
    """
        Database handler class to connect to the database and manipulate.
    """
    def __init__(self, host, port, name):
        self.port = port
        self.host = host
        self.con = self.connect(host, port)

        self.name = name
        self.db = self.database(name)

    def database(self, name):
        """
            Handler for the database supplied by the name, the connectio needs
            to be established beforehand.
        """
        self.db = self.con[name]

    def connect(self, host, port, v=True):
        try:
            self.con = Connection(host=host, port=port)
            if v:
                print('Connection performed successfuly!')
            except ConnectionFailure, e:
                sys.stderr.write('Could not connect to MongoDB: %s' % e)

    def connection_info(self):
        """
            Debbuging method to return the host and the port to which the
            database is connected or not.
        """
        return self.host, self.port

    def get_rule(self, query, multiple=False):
        """
            Rule finder on the database, it needs a dictionary has a query and
            also it can be a search for multiple results or just one.
        """
        if multiple:
            return self.db.rules.find(query)
        return self.db.rules.find_one(query)

    def rem_rule(self, query):
        self.db.rules.remove(query, safe=True)

    def get_packets(self, query, count=100):
        """
            Getting packets that are on the database.
        """
        if multiple > 0:
            results = self.db.rules.find(query)
            return results[:count]
        return self.db.rules.find_one(query)

    def rem_packets(self, query):
        self.db.packets.remove(query, safe=True)

    def get_user(self, query, multiple=False):
        """
            Method to search for the User's credentials on the database.
        """
        if multiple:
            return self.db.users.find(query)
        return self.db.users.fund_one(query)

    def rem_user(self, query):
        self.db.users.remove(query, safe=True)

    # def queryDB(self, query, collection):
    #     """
    #         Query method that will search for the ocurrence of at least one
    #         document that satisfies that query.
    #         Example of a query:
    #             q = { 'username': 'duarte',
    #                   'password': 'q2rewr325'
    #                 }
    #         This will search for the username duarte AND that password. It's a
    #         dictionary type query.
    #     """
    #     if collection is 'rules':
    #         self.db.rules.find_one(query)
    #     if collection is 'packets':
    #         self.db.packets

    def insert_document(self, docs, collection):
        """
            Insertion method for documents. It really needs to have a name and
            the collection with which it's going to insert.
        """
        if collection is 'rules':
            self.db.rules.insert(docs, safe=True)
            return True
        if collection is 'packets':
            self.db.packets.insert(docs, safe=True)
            return True
        if collection is 'creds':
            self.db.users.insert(docs, safe=True)
            return True
        else:
            return False
