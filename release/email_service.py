import sqlalchemy as sql
from email_sender import send_email, email_servers
import json
import time

from models import Rule, Counter
from models import User
from models import create_session

from time_aux import diff_time
from time_aux import getTime

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
        send_email(self.username, self.password, reason=reason)

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
        intro = 'Rules flagged for notification report: \n'
        report = intro
        if len(self.rules) == 0:
            return 'Nothing to report'

        for rule in self.rules:
            if rule.action in ["NOTIFY", 'NOTIFY_BLOCK']:
                report += self.mixRuleCounters(rule, self.counters[rule.id])
                report += '\n'

        if report == intro:
            return 'Nothing to report for now.'
        return report

    def userTime(self):
        users = self.session.query(User).all()
        if not users:
            return None
        min_diff = None
        current_time = getTime()
        print(current_time)
        for user in users:
            timestamp = user.timestmap
            if not timestamp == None:
                new_diff = diff_time(user.timestamp, new_time=current_time)
                if new_diff < min_diff:
                    min_diff = new_diff
        if min_diff == None:
            return None
        return diff_time(min_diff, new_time=current_time)


    def run(self, cycle):
        # cycle defaults to 3 hours.
        cycle = cycle*60*60 # convert hours to mins to secs
        while True:
            self.queryDB()
            report = self.makeReport()
            # self.send(report)
            print(report)
            print(getTime())
            last_login_time = self.userTime()
            print(last_login_time)
            if last_login_time == None or last_login_time > cycle:
                time.sleep(cycle)
            else:
                time.sleep(last_login_time)

if __name__ == '__main__':
    mail = Email(username, password)
    f = open('heimdall.conf')
    cycle = json.loads(f.read())['email_cycle']
    if type(cycle) == type(int):
        main.run(cycle)
    else:
        mail.run(3)
