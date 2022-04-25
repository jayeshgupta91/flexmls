from __future__ import print_function
import base64

import os.path
from bs4 import BeautifulSoup

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sheet import * 

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def mail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    try:
        email = sheetGet.cell(1,1).value
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().messages().list(
                q=f'from:{email}', userId='me').execute()
            # print(results)
            messages = results.get('messages')
            for msg in messages:
                # Get the message from its id
                txt = service.users().messages().get(
                    userId='me', id=msg['id']).execute()
                # print(txt)
                try:
                    # Get value of 'payload' from dictionary 'txt'
                    payload = txt['payload']
                    headers = payload['headers']

                    # Look for Subject and Sender Email in the headers
                    for d in headers:
                        if d['name'] == 'Subject':
                            subject = d['value']
                        if d['name'] == 'From':
                            sender = d['value']

                    # The Body of the message is in Encrypted format. So, we have to decode it.
                    # Get the data and decode it with base 64 decoder.
                    parts = payload.get('parts')[0]
                    data = parts['body']['data']
                    # print(data)
                    data = data.replace("-", "+").replace("_", "/")
                    decoded_data = base64.b64decode(bytes(data, 'UTF-8'))

                    value = decoded_data.decode("utf-8").split("\n")
                    # print(value)
                    flexmls = []
                    for s in value:
                        if s:
                            link = s[s.find("<")+1:s.find(">")]
                            if "www.flexmls.com" in link:
                                # print(link)
                                flexmls.append(link)

                    print(flexmls[0])
                    
                    sheetGet.update_cell(1,2, flexmls[0])

                except:
                    pass
                
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
    except:
        print("some error occured")


