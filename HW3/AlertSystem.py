from confluent_kafka import Consumer,Producer
import json
import mysql.connector
from cqrs import UserReadService

#configurazione consumer kafka per il consumer e il producer
consumer_config={
    'bootstrap.servers': 'kafka:9092',  # Kafka broker address
    'group.id': 'group1',  # Consumer group ID
    'auto.offset.reset': 'latest',  # Start reading from the latest message
    'enable.auto.commit': True,  # Automatically commit offsets periodically
    'auto.commit.interval.ms': 5000  # Commit offsets every 5000ms (5 seconds)
}

producer_config={
    'bootstrap.servers': 'kafka:9092',  # Kafka broker address. QUI DOVREMMO POI METTERE IL BROKER DEL DOCKER COMPOSE
    'acks': 'all',  # Ensure all in-sync replicas acknowledge the message
    'batch.size': 500,  # Maximum number of bytes to batch in a single request
    'max.in.flight.requests.per.connection': 1,  # Only one in-flight request per connection
    'retries': 3  # Retry up to 3 times on failure
}

consumer=Consumer(consumer_config)
producer=Producer(producer_config)

topic1='to-alert-system' #topic in cui prende i messaggi di ingresso
topic2='to-notifier' #topic in cui manda se c'è stato un superamento soglia

# Funzione per creare la connessione al database MySQL
def create_db_connection():
    try:
        conn = mysql.connector.connect(
            host='mysql',
            database='hw2',
            user='pippo',
            password='ciao'
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        print(f"Errore nella connessione al database: {e}")
        return None


def produce_sync(producer, topic, value):
    """
    Funzione sincrona per inviare un messaggio a Kafka.
    Blocca l'esecuzione finché il messaggio non è stato consegnato.
    
    :param producer: Istanza del producer Kafka.
    :param topic: Nome del topic Kafka a cui inviare il messaggio.
    :param value: Valore del messaggio (stringa).
    """
    try:
        # Invia il messaggio in modo sincrono
        producer.produce(topic, value)
        producer.flush()  # Blocca finché tutti i messaggi non sono stati consegnati
        print(f"Messaggio inviato su topic {topic}: {value}")
    except Exception as e:
        print(f"Errore durante l'invio del messaggio: {e}")

def alert_system():
    consumer.subscribe([topic1]) #iscrizione al topic di input
    user_read_service=UserReadService()

    while True:
        msg=consumer.poll(1.0)
        if msg is None:
            continue #nessun messaggio ricevuto, continuo il polling
        if msg.error():
            print(f"errore del consumer: {msg.error()}")
            continue

        try:
            #parsing del messaggio ricevuto
            data=json.loads(msg.value().decode('utf-8'))
            print(f"messaggio ricevuto: {data}")
            # Recupera i dati per email e ticker
            try:
                result=user_read_service.get_soglie_from_utenti(data['email'],data['ticker'])
                if result:
                    high_value=result['high_value']
                    low_value=result['low_value']

                    #controllo se il valore supera la soglia o meno
                    if high_value is not None and data['value']>high_value:
                        alert_message={
                            'email': data['email'],
                            'ticker': data['ticker'],
                            'condition': 'il valore ha superato la soglia high'
                        }
                        produce_sync(producer,topic2,json.dumps(alert_message))
                        print(f"Alert: {data['email']} - {data['ticker']} ha superato la soglia alta!")
                    elif low_value is not None and data['value']<low_value:
                        alert_message={
                            'email': data['email'],
                            'ticker': data['ticker'],
                            'condition': 'il valore è sceso sotto la soglia low'
                        }
                        produce_sync(producer,topic2,json.dumps(alert_message))
                        print(f"Alert: {data['email']} - {data['ticker']} è sceso sotto la soglia low!")
            except mysql.connector.Error as e:
                print(f"Errore durante la query al DB: {e}")    
        except Exception as er:
            print(f"Errore nel processing del messaggio: {er}")            


# Avvio dell'Alert System
if __name__ == '__main__':
    try:
        alert_system()
    except KeyboardInterrupt:
        print("Interruzione manuale ricevuta, chiusura del consumer...")
    finally:
        consumer.close()
        print("Consumer Kafka chiuso correttamente.")