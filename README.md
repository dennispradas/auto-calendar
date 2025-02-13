Codi per a enviar correus via microsoft SMTP

DEPENDENCIES PIP:
    mysql-connector-python 
    icalendar

FUNCIÓ:
    En executar llegeix dins de la sql, l'última entrada, la importa, crea un arxiu .ics i l'adjunta al correu
    Utilitza la llibreria d'SMTP, i envia el correu al servidor SMTP d'Outlook
    No necessita de cap API, tot el necessari es alla.
    Per a integrar-ho al formulari, només s'hauria de posar una linea que l'executés i ell mateix fa sol
    Es necessari configurar les linees:

    DB_CONFIG = {
    'host': '', # Host de la MySql
    'user': '', # Usuari BBDD
    'password': '',  # Passwd BBDD
    'database': ''  # DB
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
    EMAIL_PASSWORD = '' # Passwd del correu remitent
    TO_EMAIL = ['',''] # Email dels destinataris
