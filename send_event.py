import mysql.connector
from icalendar import Calendar, Event
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configuració de la DB
DB_CONFIG = {
    'host': '', 
    'user': '',    
    'password': '',  
    'database': ''  
}

DB_TABLE = {
    'table': '', # Nom de la taula de la DB
    'id': '', # Nom de la columna de l'ID
    'name': '', # Nom de la columna del nom de l'event
    'start_date': '', # Nom de la columna de la data d'inici
    'end_date': '' # Nom de la columna de la data de fi
}

# Configuració del SMTP
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
EMAIL_USER = '' # Email des d'on s'enviarà el correu
EMAIL_PASSWORD = ''
TO_EMAIL = ['',''] # Email dels destinataris

def get_last_entry():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM "+DB_TABLE['table']+" ORDER BY id DESC LIMIT 1"  # Adjusta segons la DB
    cursor.execute(query)
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row
    else:
        raise Exception("DB buida.")

def create_ics_file(event_data):
    cal = Calendar()
    event = Event()
    
    event.add('summary', event_data[DB_TABLE['name']])
    event.add('dtstart', datetime.strptime(str(event_data[DB_TABLE['start_date']]), '%Y-%m-%d %H:%M:%S'))
    event.add('dtend', datetime.strptime(str(event_data[DB_TABLE['end_date']]), '%Y-%m-%d %H:%M:%S'))
    event.add('description', f"Event: {str(event_data[DB_TABLE['name']])}")
    
    cal.add_component(event)
    
    filename = f"event_{event_data[DB_TABLE['id']]}.ics"
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    
    return filename

def send_email_with_attachment(to_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={attachment_path.split("/")[-1]}'
        )
        msg.attach(part)
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    last_event = get_last_entry()
    
    ics_file = create_ics_file(last_event)
    
    for p in TO_EMAIL:
        send_email_with_attachment(
            to_email=p,
            subject=f"Event de contracte {last_event[DB_TABLE['name']]}",
            body=f"Hola,\n\nt'enviem la data de fi del contracte: '{last_event[DB_TABLE['name']]}'. Siusplau, afegeix l'arxiu adjunt al teu calendari.\n\nSalut. \n\nAquest es un missatge automàtic, si us plau no responguis.",
            attachment_path=ics_file
        )
    
    print(f"Enviat.")