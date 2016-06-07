import sqlalchemy as sql
from email_sender import send_email, email_servers
import json
import time

from models import Rule, Counter
from models import create_session

# needs to have templates for the ports and also the which rules is violated
# inside the local area network.

class Email():
    def __init__(self, username, password):
        # must get the user's email and password for the account that will send
        # the email.
        # mus also get the email template.
        self.session = create_session()
        self.username = username
        self.password = password
        self.rules = []
        self.counters = {}
        pass

    def send(self, reason):
        send_mail(self.username, self.password, reason=reason)

    def queryDB(self):
        # it needs to import the Packet data model.
        self.rules = self.session.query(Rule).all()
        for rule in self.rules:
            counter = self.session.query(Counter).filter( \
                    Counter.rule_id == rule.id)
            self.counters[rule.id] = counter

    def mixRuleCounters(self, rule, counter):
        # check for IPs and MACs also!!!
        report = 'Rule no. {0}: {1}@{2}'.format(rule.id, rule.protocol, \
                rule.port)
        # can add here the IP or MAC if they exist != None
        action = ' with action [{0}]'.format(rule.action)
        if rule.ip:
            action = ' at {0}'.format(rule.ip.ip)
        if rule.mac:
            action = ' mac [{0}]'.format(rule.mac.mac)
        counter = ' activity -> {0}, {1}'.format(counter.packets, counter.byte)
        return report+action+counter

    def makeReport(self):
        report = 'Rules flagged for notification report: \n'
        for rule in self.rules:
            if rule.action in ["NOTIFY", 'NOTIFY_BLOCK']:
                report += self.mixRuleCounters(rule, self.counters[rule.id])
                report += '\n'
        return report


    def run(self, cycle=3):
        # cycle defaults to 3 hours.
        sleep_hours = cycle*60*60 # convert hours to mins to secs
        while True:
            self.queryDB()
            self.makeReport()
            time.sleep(cycle)

if __name__ == '__main__':
    mail = Email(username, password)
    mail.run()
    mail = Email(username, password)
