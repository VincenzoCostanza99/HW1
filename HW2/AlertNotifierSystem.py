from confluent_kafka import Consumer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Configurazione del Kafka Consumer
consumer_config = {
    'bootstrap.servers': 'kafka:9092',  # Kafka broker address
    'group.id': 'group2',  # Consumer group ID
    'auto.offset.reset': 'latest',  # Start reading from the latest message
    'enable.auto.commit': True,  # Automatically commit offsets periodically
    'auto.commit.interval.ms': 5000  # Commit offsets every 5000ms (5 seconds)
}

consumer = Consumer(consumer_config)

topic2 = 'to-notifier'  # Topic in cui il sistema consuma gli alert

# Funzione per inviare un'email
def send_email(subject, body, to_email):
    """
    Funzione per inviare un'email agli utenti notificati.
    :param subject: Oggetto dell'email.
    :param body: Corpo dell'email, contiene il contenuto della notifica.
    :param to_email: L'indirizzo email del destinatario.
    """
    from_email = 'hwdbsd99@gmail.com'  
    password = 'tkww qhza huun sewu'

    msg = MIMEMultipart()  # Crea un'email in formato multipart (per allegati e corpo)
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))  # Aggiungi il corpo dell'email (testo semplice)

    # Configura il server SMTP per l'invio delle email (usiamo Gmail)
    try:
        # Connessione al server SMTP di Gmail (porta 587 per TLS)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Avvia il TLS per una connessione sicura
        server.login(from_email, password)  # Autenticazione con il tuo account
        text = msg.as_string()  # Converte l'email in formato stringa
        server.sendmail(from_email, to_email, text)  # Invia l'email
        server.quit()  # Chiudi la connessione al server
        print(f"Email inviata a {to_email}")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

# Funzione per il Notifier System
def notifier_system():
    """
    Funzione che consuma i messaggi dal topic 'to-notifier' e invia notifiche via email.
    """
    consumer.subscribe([topic2])  # Iscriviti al topic 'to-notifier'

    while True:
        # Fai il polling per nuovi messaggi
        msg = consumer.poll(1.0)  # Attende per un massimo di 1 secondo per un nuovo messaggio
        if msg is None:
            continue  # Nessun messaggio ricevuto, continua il polling
        if msg.error():
            print(f"Errore del consumer: {msg.error()}")  # Se c'è un errore, stampalo
            continue

        try:
            # Parsing del messaggio ricevuto, decodifica il valore da JSON
            data = json.loads(msg.value().decode('utf-8'))
            print(f"Messaggio ricevuto: {data}")

            # Estrai le informazioni dall'alert (email, ticker e condition)
            email = data['email']
            ticker = data['ticker']
            condition = data['condition']

            # Costruisci il soggetto e il corpo del messaggio dell'email
            subject = f"Alert per {ticker}"  # Oggetto dell'email, con il ticker
            body = f"Ciao, \n\nIl valore del ticker {ticker} ha subito una variazione:\n\n{condition}\n\nControlla il tuo account per maggiori dettagli."

            # Invia l'email di notifica
            send_email(subject, body, email)  # Chiama la funzione per inviare l'email

        except Exception as e:
            print(f"Errore durante il processing del messaggio: {e}")  # Stampa errori durante il parsing del messaggio

# Avvio del Notifier System
if __name__ == '__main__':
    try:
        notifier_system()  # Avvia il Notifier System
    except KeyboardInterrupt:
        print("Interruzione manuale ricevuta, chiusura del consumer...")  # Gestione dell'interruzione
    finally:
        consumer.close()  # Chiude il consumer Kafka
        print("Consumer Kafka chiuso correttamente.")