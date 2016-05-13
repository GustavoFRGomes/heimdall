import smtplib
import json

email_servers = {
                 'gmail': 'smtp.gmail.com',
                 'outlook': 'smtp-mail.outlook.com',
                 'yahoo': 'smtp.mail.yahoo.com',
                 'at&t': 'smtp.mail.att.net', # port 465
                 'verizon': 'smtp.verizon.net', #port 465
                 'comcast': 'smtp.comcast.net'
                }

def send_email(username, password, provider='gmail', template='email.json', \
        reason = ''):
    port = 587 # to use the TLS conection
    if provider in ['at&t', 'verizon']:
        port = 465

    smtpObj = smtplib.SMTP(email_servers[provider]+':587')
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(username, password)

    receiver, message = parseJson(template, reason)

    smtpObj.sendmail(username, receiver, message)
    smtpObj.quit()

def parseJson(template, reason):
    text = open(template)
    temp = json.loads(text.read())['email']

    receiver = temp['email_to']
    subject = 'Subject: ' + temp['subject'] + '\n'
    message = temp['greeting'] + ' '
    message += temp['users_name'] + ',\n\n'
    if reason == '':
        message += temp['reason'] + '\n\n'
    else:
        message += reason + '\n\n'
    message += temp['goodbye'] + '\n'
    message += temp['sign']

    subject += '\n' + message
    return receiver, subject

