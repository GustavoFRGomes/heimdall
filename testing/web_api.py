import requests as req

uri = {
    "rule": "http://127.0.0.1:5000/rule/0",
    'user': 'http://127.0.0.1:5000/user'
}

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
