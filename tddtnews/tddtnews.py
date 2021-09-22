import os.path
import base64

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from urllib.error import HTTPError
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class EmailSender():

    def __init__(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        #Resource for interacting with API
        self.service = build('gmail', 'v1', credentials=creds) 
    
    def create_message(self, to, sender, subject, cc, message_text):
        message = MIMEText(message_text,'html')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message['cc'] = cc
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message(self, user_id, message):
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message)
                    .execute())
            print(f"Message Id: {message['id']}")
            return message
        except HTTPError as error:
            print(f"An error occurred: {error}")


def main():
    sender = EmailSender()
    with open("example.html", "r") as ex:
        message = sender.create_message("ben@tddt.org", "ben@tddt.org", "test", "ben@tddt.org", ex.read())
        sender.send_message("ben@tddt.org", message)

if __name__ == '__main__':
    main()