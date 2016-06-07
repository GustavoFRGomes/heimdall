import requests as req
from requests.auth import HTTPBasicAuth
import json

uri = {
    "rule": "https://127.0.0.1:5000/rule/",
    "rules": 'https://127.0.0.1:5000/rules',
    'counters': 'https://127.0.0.1:5000/counters',
    'counter': 'https://127.0.0.1:5000/counter'
}

USERNAME = ''
PASSWORD = ''
VERIFY = False

def cert_path(filename):
    """
        Defines path to the certificate file.
    """
    VERIFY = filename

def set_username(username):
    USERNAME = username

def set_password(password):
    PASSWORD = password

def authenticator():
    if not (USERNAME == '' and PASSWORD == ''):
        return USERNAME, PASSWORD
    return '', ''

def getRule(rule_id, auth=True, https=True):
    """
        Get a Rule from a specific ID.
    """
    url = uri['rule'] + str(rule_id)
    response = req.get(url, auth=authenticator(), verify=VERIFY)
    # print(response)
    return response

def deleteRule(rule_id):
    """
        Delete a Rule on the web server.
    """
    url = uri['rule'] + str(rule_id)
    response = req.delete(url, auth=authenticator(), verify=VERIFY)
    # print(response)
    return response

def editRule(rule_id, port, action, protocol, ip=None, mac=None):
    """
        Edit a Rule at the web service.
    """
    rule['port'] = port
    rule['protocol'] = protocol
    rule['action'] = action
    if not ip:
        rule['ip'] = ip
    if not mac:
        rule['mac'] = mac

    msg = json.dumps(rule)
    url = uri['rule'] + str(rule_id)
    response = req.put(url, json=msg, auth=authenticator(), verify=VERIFY)
    # print(response)
    return response

def listRules():
    """
        Function to list all of the rules.
    """
    url = uri['rules']
    response = req.get(url, auth=authenticator(), verify=VERIFY)
    # print(response)
    return response

def postRule(port, action, protocol, ip=None, mac=None):
    """
        Append a Rule to the web server.
    """
    rule = {}
    rule['port'] = port
    rule['protocol'] = protocol
    rule['action'] = action
    if ip:
        rule['ip'] = ip
    if mac:
        rule['mac'] = mac

    msg = json.dumps(rule)
    print(msg)
    url = uri['rules']
    response = req.post(url, msg, auth=authenticator(), verify=VERIFY)
    # print(response.text)
    return response

def man_addRule():
    print('Port: ')
    port = input()

    print('Protocol:')
    protocol = input()

    print('Action:')
    action = input()

    print('IP:')
    ip = input()
    if not ip == '':
        print('IPv4?')
        ipv4 = input()

    print('Mac:')
    mac = input()

def addIp(ip, ipv4):
    return {'ip': ip, 'ipv4':ipv4}

def addMac(mac):
    return {'mac': mac}

def addUser(username, password):
    user = {'username':username, 'password':password}
    req.post(uri['user'], user)
