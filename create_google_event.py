import mysql.connector
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

# Configuración de la base de datos MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'local',
    'password': 'dp3879dp',
    'database': 'form'
}

# Alcances requeridos para Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    """Autenticar con Google Calendar API."""
    print("[INFO] Autenticando con Google Calendar API...")
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    print("[INFO] Autenticación completada.")
    return creds

def get_last_event():
    """Obtener el último evento insertado en la base de datos."""
    print("[INFO] Conectando a la base de datos...")
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM eventos ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    
    event = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if event:
        print("[INFO] Último evento obtenido:", event)
    else:
        print("[ERROR] No se encontró ningún evento.")
    
    return event

def create_google_event(event):
    """Crear un evento en Google Calendar."""
    print("[INFO] Creando evento en Google Calendar...")
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    fecha_inicio_iso = event['fecha_inicio'].isoformat()
    fecha_fin_iso = event['fecha_fin'].isoformat()

    event_data = {
        'summary': event['nombre'],
        'start': {'dateTime': fecha_inicio_iso, 'timeZone': 'UTC'},
        'end': {'dateTime': fecha_fin_iso, 'timeZone': 'UTC'},
        'attendees': [{'email': event['email']}],
        'reminders': {'useDefault': True},
    }

    created_event = service.events().insert(calendarId='primary', body=event_data).execute()
    
    print(f"[INFO] Evento creado: {created_event.get('htmlLink')}")

if __name__ == '__main__':
    last_event = get_last_event()
    
    if last_event:
        create_google_event(last_event)
