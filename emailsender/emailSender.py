import base64

from googleapiclient.discovery import build

from urllib.error import HTTPError
from email.mime.text import MIMEText
from tddtnews.googleAuth import googleAuth


class emailSender():

    def __init__(self):

        auth = googleAuth()
        #Resource for interacting with API
        self.service = build('gmail', 'v1', credentials=auth.get_creds()) 
    
    def create_message(self, to, sender, subject, cc, message_text):
        message = MIMEText(message_text,'html')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message['cc'] = cc
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message(self, message, user_id="me"):
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message)
                    .execute())
            print(f"Message Id: {message['id']}")
            return message
        except HTTPError as error:
            print(f"An error occurred: {error}")