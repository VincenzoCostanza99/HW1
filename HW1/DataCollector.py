import yfinance as yf
from mysql.connector import Error
import mysql.connector
from datetime import datetime
from CircuitBreaker import circuit_breaker, CircuitBreakerOpenException
import time

# Configura il Circuit Breaker
circuit_breaker = circuit_breaker(failure_threshold=5, recovery_timeout=30)

def create_connection():
    try:
        connessione=mysql.connector.connect(
            host='mysql',
            database='hw1',
            user='pippo',
            password='ciao'
        )
        if connessione.is_connected():
            return connessione
    except mysql.connector.Error as e:
        print(f"errore nella connessione del database:{e}")
        return None

#funziona per gli utenti dal db hw1
def preleva_utenti_da_hw1():
    connessione=create_connection()
    utenti=[]
    if connessione:
        cursor=connessione.cursor()
        try:
            #recupero i dati inerenti agli utenti nel db
            cursor.execute("SELECT email,ticker FROM utenti")       
            utenti=cursor.fetchall() #restituisce una lista di tuple che contiene l'email con il rispettivo ticker
        except Error as e:
            print(f"Errore durante il recupero dal db degli utenti: {e}")
        finally:
            cursor.close()
            connessione.close()
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

        if not utenti:
            print("il db è vuoto e non ci sono utenti")
            return None
        for email,ticker in utenti:
            print(f"recupero i dati per l'utente: {email} con ticker: {ticker}")

            #passo all'inserimento dei dati nel db HW1
            connessione=create_connection()
            if connessione:
                cursor=connessione.cursor()
                try:
                    #a questo punto chiamo il circuit breaker
                    ultimo_valore,timestamp= circuit_breaker.call(recupero_dati,ticker)
                    cursor.execute("INSERT INTO dati_finanziari (email,ticker,valore) VALUES (%s,%s,%s)",(email,ticker,ultimo_valore))#timestamp lo aggiunge il db quindi non serve metterlo
                    connessione.commit() #salvo le modifiche
                    print(f"dati per utente: {email} con ticker:{ticker} inseriti con successo")
                except Error as e:
                    print(f"errore durante l'inserimento dei dati:{e}")
                except CircuitBreakerOpenException:
                    print(f"non è stato possibile recuperare i dati per {ticker}- il circuit breaker è open")        
                finally:
                    cursor.close()
                    connessione.close()     
        # Aspetta 60 secondi prima di ripetere il processo
        time.sleep(60)                   

if __name__ =='__main__':
    inserimento_dati()