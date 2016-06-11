from getpass import getpass
from user_handler import addUser
import json

from firewall import Firewall
from email_service import Email
from api import app

import os
from multiprocessing import Process

def add_user():
    print('Can you please tell us your name?')
    name = input('Name: ')
    print('Add one user to the system')
    username = input('Username: ')
    password = getpass('Password: ')

    return name, username, password

def add_email():
    print('Please let us know of a contact email below!')
    email = input('Email: ')
    print('We now ask that you specify a time cycle, in hours.')
    email_cycle = input('Cycle: ')
    return email, email_cycle

def firewall_cycle():
    print('Please, in seconds, specify the update cycle for the firewall.')
    cycle = input('Cycle [/s]: ')
    return cycle

def prompt_user():
    config_data = {}
    print("Welcome to Heimdall's configuration assistant!")
    print("we only need a few details of you")
    name, username, password = add_user()
    email, email_cycle = add_email()
    fwl_cycle = firewall_cycle()

    config_data['name'] = name
    config_data['email'] = email
    config_data['email_cycle'] = int(email_cycle)
    config_data['firewall_cycle'] = int(fwl_cycle)

    addUser(username, password)
    f = open('email.json', 'r')
    email_json = json.loads(f.read())
    email_json['email']['email_to'] = config_data['email']
    email_json['email']['users_name'] = config_data['name']
    with open('email.json', 'w') as f:
        json.dump(email_json, f, indent=4)

    with open('heimdall.conf', 'w+') as f:
        json.dump(config_data, f, indent=4)

def run():
    if not (os.path.isfile('./heimdall.conf')):
        prompt_user()
    f = open('./heimdall.conf')
    config = json.loads(f.read())

    print(config)
    firewall = Firewall(chain='FORWARD')
    email = Email(config['mail_username'], config['mail_password'])
    p_firewall = Process(target=firewall.run, \
            args=(config['firewall_cycle'],))
    p_email = Process(target=email.run, args=(config['email_cycle'],))
    p_firewall.start()
    p_email.start()
    os.system('python api.py')

if __name__ == '__main__':
    # prompt_user()
    run()
