import grpc
import protoBuffer_pb2
import protoBuffer_pb2_grpc
from concurrent import futures
from threading import Lock
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection= mysql.connector.connect(
            host='mysql',
            database='hw1',
            user='pippo',
            password='ciao'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Errore nella connessione al database: {e}")
        return None
    
requestEmail_cache = {}
# A lock to synchronize access to the cache for thread safety
cache_lock = Lock()

class UserService(protoBuffer_pb2_grpc.UserServiceServicer):
    def Registrazione_utente(self,request,context):
        email=request.email
        ticker=request.ticker

        print(f"registrazione utente con email: {email}")
        #qui è implementato l'at most once
        with cache_lock:
            print("Cache content:\n")
            print(requestEmail_cache)
            if email in requestEmail_cache:
                print(f"Returning cached response for email {email}")
                return email

        #registrazione nuovo utente
        print(f"sto processando una nuova richiesta con email={request.email}, ticker={request.ticker}")
        connection= create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("INSERT INTO utenti(email,ticker) VALUES (%s,%s)",(email,ticker))
                connection.commit()
                cursor.close()
                response = protoBuffer_pb2.Registrazione_utente_Reply(messaggio="l'utente si è registrato con successo", stato_registrazione="success")
                with cache_lock:
                    requestEmail_cache[email]=ticker
                    print(requestEmail_cache)        
                return response    
            except Error as e:
                print(f"errore durante la registrazione:{e}")
                response = protoBuffer_pb2.Registrazione_utente_Reply(messaggio="errore durante la registrazione", stato_registrazione="failed")
                return response
            finally:
                connection.close()

    def Aggiornamento_utente(self, request, context):
        print(f"nuovo aggiornamento utente con email: {request.email}, ticker: {request.ticker}")
        #qui è implementato l'at most once
        with cache_lock:
            if request.email in requestEmail_cache:
                if request.ticker in requestEmail_cache[request.email]:
                    print(f"la preferenza dell'utente: {request.email} non è cambiata")
                    print("quindi il contenuto della cache è:\n")
                    print(requestEmail_cache)
                    return request.email
        
        #AGGIORNAMENTO TICKER DELL'UTENTE GIA ISCRITTO
        print(f"sto effettuando un aggiornamento del ticker, con email={request.email}, ticker={request.ticker}")
        connection= create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("UPDATE utenti SET ticker=%s WHERE email=%s",(request.ticker,request.email))
                connection.commit()
                cursor.close()
                response = protoBuffer_pb2.Aggiornamento_utente_Reply(messaggio="il ticker è stato aggiornato con successo", stato_aggiornamento="success")
                with cache_lock:
                    requestEmail_cache[request.email]=request.ticker
                    print(requestEmail_cache)        
                return response    
            except Error as e:
                print(f"errore durante l'aggiornamento':{e}")
                response = protoBuffer_pb2.Aggiornamento_utente_Reply(messaggio="errore durante l'aggiornamento'", stato_registrazione="failed")
                return response
            finally:
                connection.close()

    def Delete_utente(self, request, context):
        email=request.email
        print(f"cancellazione utente con email: {email}")
        with cache_lock:
            if email in requestEmail_cache:
                del requestEmail_cache[email]
                print(f"sto effettuando il delete dell'utente con email={email}")
                connection= create_connection()
                if connection:
                    cursor=connection.cursor()
                    try:
                        cursor.execute("DELETE FROM utenti WHERE email=%s",(email,))
                        connection.commit()
                        cursor.close()
                        response = protoBuffer_pb2.Delete_utente_Reply(messaggio="l'utente è stato eliminato con successo", stato_delete="success")
                        return response    
                    except Error as e:
                        print(f"errore durante l'eliminazione':{e}")
                        response = protoBuffer_pb2.Delete_utente_Reply(messaggio="errore durante l'eliminazione'", stato_delete="failed")
                        return response
                    finally:
                        connection.close()
            else:
                print("l'utente non è presente, infatti guardando la cache ho il seguente contenuto:")
                return print(requestEmail_cache)
    
    def Get_Last_Value(self, request, context):
        #recupero l'ultimo valore del ticker a cui l'utente è interessato
        email=request.email
        ticker=request.ticker
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("SELECT valore FROM dati_finanziari WHERE email=%s AND ticker=%s ORDER BY timestamp DESC LIMIT 1",(email,ticker))
                result=cursor.fetchone()
                if result is None:
                    print("non è presente nessun valore inerenete a questi dati quindi:\n")
                    return protoBuffer_pb2.Get_Last_Value_utente_Reply(res=-1) #ritorna -1 se nessun valore è stato trovato
                else:
                    return protoBuffer_pb2.Get_Last_Value_utente_Reply(res=result[0])
            except Error as err:
                print(f"Errore durante la connessione al database:{err}")
                return protoBuffer_pb2.Get_Last_Value_utente_Reply(res=-1)  #Codice di errore
            finally:
                cursor.close()
                connection.close()

    def Get_Media(self, request, context):
        email=request.email
        ticker=request.ticker
        num_valori=request.num_valori
        connection=create_connection()
        if connection:
            cursor=connection.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM dati_finanziari WHERE email=%s AND ticker=%s",(email,ticker))
                count_result=cursor.fetchone()
                if count_result is None or count_result[0]==0:
                    #non è stato trovato nessun valore inerente al ticker e alla mail
                    print("il numero di valori presente per quel ticker è 0 \n")
                    return protoBuffer_pb2.Get_Media_utente_Reply(media=-1)
                valori_tot=count_result[0]
                if num_valori> valori_tot:
                    print(f"il numero di valori richiesto ({num_valori}) è maggiore dei valori disponibili ({valori_tot})")
                    return protoBuffer_pb2.Get_Media_utente_Reply(media=-1)
                
                cursor.execute("SELECT valore FROM dati_finanziari WHERE email=%s AND ticker=%s ORDER BY timestamp DESC LIMIT %s",(email,ticker,num_valori))
                result=cursor.fetchall()
                if result is None or len(result)==0:
                    return protoBuffer_pb2.Get_Media_utente_Reply(media=-1) #ritorna -1 se nessun valore è stato trovato
                else:
                    values=[row[0] for row in result]
                    valore_media=sum(values)/num_valori
                    return protoBuffer_pb2.Get_Media_utente_Reply(media=valore_media)
            except Error as err:
                print(f"Errore durante il calcolo della media:{err}")
                return protoBuffer_pb2.Get_Media_utente_Reply(media=-1)
            finally:
                cursor.close()
                connection.close()                

def serve():
    port = '50051'
    # Initialize a thread pool with 10 workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Register the UserService with the server
    protoBuffer_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    # Bind the server to the specified port
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("UserService started, listening on " + port)
    server.wait_for_termination()

if __name__=='__main__':
    serve()