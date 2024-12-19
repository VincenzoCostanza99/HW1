from confluent_kafka import Producer
import yfinance as yf
from mysql.connector import Error
from CircuitBreaker import circuit_breaker, CircuitBreakerOpenException
import time
import json
from cqrs import(
    FinancialWriteService,UserReadService,
    AddDatiFinanziariCommand
) 
# Configura il Circuit Breaker
circuit_breaker = circuit_breaker(failure_threshold=5, recovery_timeout=30)

#configurazione Kafka Producer
producer_config={
    'bootstrap.servers': 'kafka:9092',  # Kafka broker address.
    'acks': 'all',  # Ensure all in-sync replicas acknowledge the message
    'batch.size': 500,  # Maximum number of bytes to batch in a single request
    'max.in.flight.requests.per.connection': 1,  # Only one in-flight request per connection
    'retries': 3  # Retry up to 3 times on failure
}

producer=Producer(producer_config)
topic1='to-alert-system'

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
        print(f"Messaggio inviato sincronicamente al topic {topic}: {value}")
    except Exception as e:
        print(f"Errore durante l'invio del messaggio: {e}")

#funziona per gli utenti dal db hw1
def preleva_utenti_da_hw1():
    user_read_service=UserReadService()
    utenti=[]
    try:
        #recupero i dati inerenti agli utenti nel db
        utenti=user_read_service.get_all_users()
    except Error as e:
        print(f"Errore durante il recupero dal db degli utenti: {e}")
    return utenti    

def recupero_dati(ticker):
    #recupero i dati inerenti al ticker usando yFinance e prendo i dati relativi ad un giorno
    stock=yf.Ticker(ticker)
    dati= stock.history(period="1d")  
    if not dati.empty:
        #accedo all'ultimo valore della colonna 'Close' di un DataFrame Pandas denominato dati
        ultimo_valore=dati['Close'].iloc[-1]
        timestamp=dati.index[-1] #mi prendo il timestamp dell'ultimo valore
        return ultimo_valore,timestamp
    else:
        raise Exception(f"nessun dato disponibile per {ticker}")

#adesso implementiamo una funzione per raccogliere i dati finanziari in base al ticker usando yFinance
def inserimento_dati():
    #a questo punto eseguiamo il data collector che recupera i dati e li salva in hw1
    while True:
        #recupero i dati degli utenti
        utenti=preleva_utenti_da_hw1()
        financial_write_service=FinancialWriteService()

        if not utenti:
            print("il db è vuoto e non ci sono utenti")
            return None
        for email,ticker in utenti:
            print(f"recupero i dati per l'utente: {email} con ticker: {ticker}")

            #passo all'inserimento dei dati nel db HW1
            try:
                #a questo punto chiamo il circuit breaker
                ultimo_valore,timestamp= circuit_breaker.call(recupero_dati,ticker)
                command=AddDatiFinanziariCommand(email,ticker,ultimo_valore)
                financial_write_service.handle_add_financial_data(command)
                print(f"dati per utente: {email} con ticker:{ticker} inseriti con successo")
                #passiamo alla produzione del messaggio su kafka
                message={
                    'email':email,
                    'ticker':ticker,
                    'value':ultimo_valore
                }
                produce_sync(producer, topic1, json.dumps(message))
            except Error as e:
                print(f"errore durante l'inserimento dei dati:{e}")
            except CircuitBreakerOpenException:
                print(f"non è stato possibile recuperare i dati per {ticker}- il circuit breaker è open")        
        # Aspetta 5 minuti prima di ripetere il processo
        time.sleep(60)                   

if __name__ =='__main__':
    inserimento_dati()