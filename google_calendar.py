from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_google_credentials():
    """Gets valid user credentials from storage or initiates OAuth flow."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                'credentials.json',
                SCOPES,
                redirect_uri='http://localhost:8080/auth/google/callback'
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            return None, auth_url
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds, None

def get_calendar_service(creds):
    """Build and return the Google Calendar API service."""
    return build('calendar', 'v3', credentials=creds)

def get_events(service, max_results=10):
    """Get upcoming events from the user's primary calendar."""
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

def format_event(event):
    """Format a Google Calendar event into our application's format."""
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    
    return {
        'id': event['id'],
        'title': event['summary'],
        'description': event.get('description', ''),
        'start_time': start,
        'end_time': end,
        'location': event.get('location', ''),
        'status': 'pending'  # Default status for imported events
    } 