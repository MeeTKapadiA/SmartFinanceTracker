import os.path
import base64
import json
from typing import List, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.core.config import settings

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class EmailService:
    def __init__(self):
        self.creds = None
        self.service = None
        
    def authenticate(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception:
                    print("Token expired and refresh failed.")
                    self.creds = None
            
            if not self.creds:
                # Check for client_secret.json or env vars
                if os.path.exists('client_secret.json'):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secret.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                elif settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
                    # Construct client config from env vars
                    client_config = {
                        "installed": {
                            "client_id": settings.GOOGLE_CLIENT_ID,
                            "client_secret": settings.GOOGLE_CLIENT_SECRET,
                            "project_id": "finance-tracker",
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "redirect_uris": ["http://localhost"]
                        }
                    }
                    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                else:
                    print("No credentials found. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET or provide client_secret.json")
                    return False
            
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=self.creds)
        return True

    def get_messages(self, limit: int = 10) -> List[dict]:
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            results = self.service.users().messages().list(userId='me', maxResults=limit).execute()
            messages = results.get('messages', [])
            
            full_messages = []
            for msg in messages:
                txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                full_messages.append(txt)
            return full_messages
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_message_body(self, message: dict) -> str:
        try:
            payload = message['payload']
            if 'parts' in payload:
                parts = payload['parts']
                data = parts[0]['body']['data']
            else:
                data = payload['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)
            return decoded_data.decode("utf-8")
        except Exception:
            return ""

email_service = EmailService()
