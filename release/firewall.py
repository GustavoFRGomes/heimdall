import iptc
import time
from time_aux import getTime # create a timestamp getter returns string
from models import create_session
from models import Rule, IP, MAC
from models import Counter

from time_aux import diff_time

class Firewall():

    def __init__(self, chain='FORWARD'):
        self.session = create_session()
        self.table = iptc.Table(iptc.Table.FILTER)
        self.chain = iptc.Chain(self.table, chain)
        self.rules = None

    def getFromDB(self):
        return self.session.query(Rule).all()

    def flushRules(self):
        """
        Method to flush all of the rules within the chain.
        """
        self.chain.flush()

    def submitRule(self, rule):
        """
            Method to insert one rule at a time into the chain.
        """
        self.chain.insert_rule(rule)

    def resetCounters(self):
        """
        Method that will zero all of the counters for the rule set and drop them
        from the Database because of the result.
        """
        self.chain.zero_counters()
        self.session.begin()
        counters = self.session.query(Counter).all()
        self.session.query(Counter).delete()
        self.session.commit()

    def addIp(self, rule, ip):
        """
            Method to add an IP address to a specific rule. It receives the
            iptc.Rule and the IP address in as a models.IP instance.
        """
        if ip.src:
            # Source address so
            rule.src = ip.ip
        else:
            rule.dst = ip.ip

    def addMac(self, rule, mac):
        """
            Method that adds a MAC address to a rule. Receives the iptc.Rule and
            an instance of the models.MAC class.
        """
        match = iptc.Match(rule, 'mac')
        match.mac_source = mac
        rule.add_match(match)

    def ruleUpdate(self):
        rules = self.getFromDB()
        if not self.rules == rules:
            self.rules = rules
            self.table.autocommit = False
            self.flushRules()
            self.resetCounters() # reset all the counters
            for rule in self.rules:
                valid, r = self.addRule(rule)
                if (valid):
                    self.submitRule(r)
            self.table.commit()
            self.table.autocommit = True
            self.table.refresh()

    def addRule(self, db_rule):
        rule = iptc.Rule()
        try:
            rule.protocol = db_rule.protocol
            match = rule.create_match(db_rule.protocol)
            match.dport = str(db_rule.port)
            if db_rule.ip:
                rule.src = db_rule.ip.ip
            if db_rule.mac:
                mac_match = rule.create_match('mac')
                mac_match.mac_source = db_rule.mac.mac
            if db_rule.action in ['ACCEPT', 'NOTIFY']:
                rule.target = iptc.Target(rule, 'ACCEPT')
            if db_rule.action in ['BLOCK', 'BLOCK_NOTIFY']:
                print(db_rule.action)
                rule.target = iptc.Target(rule, 'DROP')
        except iptc.xtables.XTablesError:
            return False, None
        return True, rule

    def createRule(self, rule_dic):
        rule = iptc.Rule()
        protocol = rule_dic['protocol']
        rule.protocol = protocol
        match = rule.create_match(protocol)
        match.dport = str(rule_dic['port'])
        if db_rule.action in ['ACCEPT', 'NOTIFY']:
            rule.target = iptc.Target(rule, 'ACCEPT')
        if db_rule.action in ['BLOCK', 'BLOCK_NOTIFY']:
            rule.target = iptc.Target(rule, 'DROP')

        # self.chain.insert_rule(rule)
        return rule

    def counterDB(self, results):
        # add the id of the rule and the packets and bytes from the tuple
        # respectively!
        rules = self.getFromDB()
        # print(rules)
        # check for mismatch between counters and rules.
        self.session.begin()
        for index in range(len(rules)):
            # print('REsultados')
            # print(results[index])
            pair = results[index]
            print(pair)
            counter = Counter(rule_id=rules[index].id, timestamp=getTime(), \
                    packets=pair[0], byte=pair[1])
            # print(counter.rule_id, counter.timestamp, counter.packets)
            self.session.add(counter)

        self.session.commit()

    def counterUpdate(self):
        results = []
        self.table.refresh()
        for rule in self.chain.rules:
            results.append(rule.get_counters())
            # print(results[-1])
        self.counterDB(results)

    def run(self, cycle):
        while True:
            self.ruleUpdate()
            self.counterUpdate()
            # print('Starting')
            time.sleep(cycle) # 30 secon wait

if __name__ == '__main__':
    firewall = Firewall()
    firewall.run(30)
