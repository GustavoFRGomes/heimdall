import iptc
import time
from time_aux import getTime # create a timestamp getter returns string
from models import create_session
from models import Rule, Counter

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
        """
        Method to flush all of the rules within the chain.
        """
        self.chain.flush()

    def submitRule(self, rule):
        self.chain.insert_rule(rule)

    def resetCounters(self):
        """
        Method that will zero all of the counters for the rule set and drop them
        from the Database because of the result.
        """
        self.chain.zero_counters()
        counters = self.session.query(Counter).all()
        self.session.query(Counter).delete()

    def ruleUpdate(self):
        rules = self.getFromDB()
        if not self.rules == rules:
            self.rules = rules
            self.resetCounters() # reset all the counters
            self.table.autocommit = False
            for rule in self.rules:
                r = self.createRule(rule)
                submirRule(r)
            self.table.commit()
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
            rule.target = iptc.Target(rule, 'ACCEPT')
        if rule_dic['action'] == 'BLOCK_NOTIFY':
            rule.target = iptc.Target(rule, 'BLOCK')

        # self.chain.insert_rule(rule)
        return rule

    def counterDB(self, results):
        # add the id of the rule and the packets and bytes from the tuple
        # respectively!
        rules = self.getFromDB()
        for rule, pair in zip(rules, results):
            counter = Counter(rule_id=rule.id, timestamp=getTime(), \
                    packets=pair[0], byte=pair[1])
            self.session.add(counter)

    def counterUpdate(self):
        results = []
        for rule in self.chain.rules:
            results.append(rule.get_counters())
        self.counterDB(results)

    def run(self, rest_time=30):
        while True:
            self.ruleUpdate()
            # self.counterUpdate()
            time.sleep(30) # 30 secon wait

if __name__ == '__main__':
    firewall = Firewall()
    firewall.run(rest_time=30)
