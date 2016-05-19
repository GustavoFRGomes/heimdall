import iptc
from models import create_session
from models import Rule

class Firewall():

    def __init__(self):
        self.session = create_session()
        self.table = iptc.Table(iptc.Table.FILTER)
        self.chain = iptc.Chain(self.table, "INPUT")
        self.rules = None
        pass

    def getFromDB(self):
        return self.session.query(Rule).all()

    def flushRules(self):
        pass

    def submitRule(self, rule):
        self.chain.insert_rule(rule)

    def ruleUpdate(self):
        rules = self.getFromDB()
        if not self.rules == rules:
            self.rules = rules
            self.table.autocommit = False
            for rule in self.rules:
                self.createRule(rule)
            self.table.commi()
            self.table.autocommit = True

    def createRule(self, rule_dic):
        rule = iptc.Rule()
        protocol = rule_dic['protocol']
        rule.protocol = protocol
        match = rule.create_match(protocol)
        match.dport = str(rule_dic['port'])
        if rule_dic['action'] in ['DROP', 'ACCEPT']:
            rule.target = iptc.Target(rule, rule_dic['action'])
        # check for action DROP_NOTIFY
        if rule_dic['action'] == 'NOTIFY':
            # do only log action
            pass
        if rule_dic['action'] == 'BLOCK_NOTIFY':
            rule.target = iptc.Target(rule, 'BLOCK')

        self.chain.insert_rule(rule)

    def run(self, rest_time=30):
        while True:
            self.ruleUpdate()
            time.sleep(30) # 30 secon wait

if __name__ == '__main__':
    firewall = Firewall()
    firewall.run(rest_time=30)
