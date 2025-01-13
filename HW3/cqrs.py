import mysql.connector
from mysql.connector import Error
import time
import sys

def create_connection():
    try:
        connection= mysql.connector.connect(
            host='mysql',
            database='hw2',
            user='pippo',
            password='ciao'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Errore nella connessione al database: {e}")
        return None

def wait_for_db_ready(retries=10, delay=2):
    """
    Aspetta che il database sia pronto prima di continuare.
    Se il database non è pronto dopo i tentativi, ferma il server.
    """
    for attempt in range(retries):
        connection = create_connection()
        if connection:
            connection.close()
            print("Database pronto.")
            return True
        print(f"Database non pronto, tentativo {attempt + 1}/{retries}. Riprovo tra {delay} secondi...")
        time.sleep(delay)
    
    # Se il database non è pronto dopo tutti i tentativi, fermiamo il server
    print("Database non è pronto dopo diversi tentativi.")
    sys.exit(1)  # Uscita con codice di errore

class AddUserCommand:
    def __init__(self,email,ticker,high_value,low_value):
        self.email=email
        self.ticker=ticker
        self.high_value=high_value
        self.low_value=low_value

class UpdateUserSogliaCommand:
    def __init__(self,email,high_value,low_value):
        self.email=email
        self.high_value=high_value
        self.low_value=low_value

class UpdateUserCommand:
    def __init__(self,email,ticker,high_value,low_value):
        self.email=email
        self.ticker=ticker
        self.high_value=high_value
        self.low_value=low_value

class DeleteUserCommand:
    def __init__(self,email):
        self.email=email

class AddDatiFinanziariCommand:
    def __init__(self,email,ticker,valore):
        self.email=email
        self.ticker=ticker
        self.valore=valore        

class UserWriteService:
    def handle_add_user(self,command):
        #registrazione utente
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("INSERT INTO utenti(email,ticker,high_value,low_value) VALUES (%s,%s,%s,%s)",(command.email,command.ticker,command.high_value,command.low_value))         
                connection.commit()
                cursor.close()
            finally:
                connection.close()    

    def handle_update_user(self, command):
        #aggiornamento utente ticker
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("UPDATE utenti SET ticker=%s,high_value=%s,low_value=%s WHERE email=%s",(command.ticker,command.high_value,command.low_value,command.email))
                connection.commit()
                cursor.close()
            finally:
                connection.close()

    def handle_update_soglia_user(self, command):
        #aggiornamento utente per sogli*
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("UPDATE utenti SET high_value=%s,low_value=%s WHERE email=%s",(command.high_value,command.low_value,command.email))
                connection.commit()
                cursor.close()
            finally:
                connection.close()    

    def handle_delete_user(self, command):
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("DELETE FROM utenti WHERE email=%s",(command.email,))
                connection.commit()
                cursor.close()
            finally:
                connection.close()

class FinancialReadService:

    def get_last_value(self,email,ticker):
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("SELECT valore FROM dati_finanziari WHERE email=%s AND ticker=%s ORDER BY timestamp DESC LIMIT 1",(email,ticker))
                result=cursor.fetchone()
                return result
            finally:
                cursor.close()
                connection.close()

    def get_num_righe_AND_get_valor(self,email,ticker,num_valori):
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM dati_finanziari WHERE email=%s AND ticker=%s",(email,ticker))
                count_result=cursor.fetchone()
                cursor.execute("SELECT valore FROM dati_finanziari WHERE email=%s AND ticker=%s ORDER BY timestamp DESC LIMIT %s",(email,ticker,num_valori))
                result=cursor.fetchall()
                return count_result,result
            finally:
                cursor.close()
                connection.close()

class UserReadService:
    def get_all_users_per_cache(self):
        if not wait_for_db_ready():
            print("impossibile connettersi al database. cache non sincronizzata")        
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                #recupera tutti gli utenti dal db
                cursor.execute("SELECT email, ticker, high_value, low_value FROM utenti")
                rows=cursor.fetchall()
                return rows
            finally:
                cursor.close()
                connection.close()
        else:
            print("Connessione al database fallita. Cache non sincronizzata")   

    def get_all_users(self):
        connessione=create_connection()
        if connessione:
            cursor=connessione.cursor()
            try:
                #recupero i dati inerenti agli utenti nel db
                cursor.execute("SELECT email,ticker FROM utenti")
                return cursor.fetchall()
            finally:
                cursor.close()
                connessione.close()

    def get_soglie_from_utenti(self,email,ticker):
        conn=create_connection()
        if conn:
            cursor=conn.cursor(dictionary=True)
            try:
                # Query per avere i valori delle soglie
                cursor.execute("SELECT high_value,low_value FROM utenti WHERE email=%s AND ticker=%s", (email, ticker))
                result=cursor.fetchone()
                return result
            finally:
                cursor.close()
                conn.close()


class FinancialWriteService:
    def handle_add_financial_data(self,command):
        connessione=create_connection()
        if connessione:
            cursor=connessione.cursor()
            try:
                cursor.execute("INSERT INTO dati_finanziari (email,ticker,valore) VALUES (%s,%s,%s)",(command.email,command.ticker,command.valore))
                connessione.commit()
            finally:
                cursor.close()
                connessione.close()    
        
