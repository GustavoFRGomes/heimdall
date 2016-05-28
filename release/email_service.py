import sqlalchemy as sql
from email_sender import send_email, email_servers
import json

# needs to have templates for the ports and also the which rules is violated
# inside the local area network.

class Email():
    def __init__(self):
        # must get the user's email and password for the account that will send
        # the email.
        # mus also get the email template.
        pass

    def send(self, reason):
        pass

    def queryDB(self):
        # it needs to import the Packet data model.
