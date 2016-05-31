import requests as req

uri = {
    "rule": "http://127.0.0.1:5000/rule/0",
    'user': 'http://127.0.0.1:5000/user'
}

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

def addRule(port, action, protocol):
    rule = {'port':port, 'protocol':protocol, 'action':action}
    req.post(uri['rule'], json=rule)

def getRule(id):
    response = req.get(uri['rule']+'/'+str(id))
    print('Response:')
    print(response.text)

def addUser(username, password):
    user = {'username':username, 'password':password}
    req.post(uri['user'], user)
