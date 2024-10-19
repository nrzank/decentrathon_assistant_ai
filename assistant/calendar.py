import os
from urllib.request import Request

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from google.oauth2.credentials import Credentials


# Авторизация в Google API
def get_calendar_service():
    creds = None
    # Файл token.json сохраняет учетные данные пользователя
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file('credentials.json')
            creds = flow.run_local_server(port=0)
        # Сохранение учетных данных в файл
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build('calendar', 'v3', credentials=creds)


# Создание события в календаре
def create_calendar_event(summary, start_time, end_time):
    service = get_calendar_service()

    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event
