import grpc
import protoBuffer_pb2
import protoBuffer_pb2_grpc
from concurrent import futures
from threading import Lock
from mysql.connector import Error
import re
from cqrs import(
    UserWriteService,FinancialReadService,
    UserReadService,AddUserCommand,
    UpdateUserCommand,DeleteUserCommand,
    UpdateUserSogliaCommand
)

def sync_cache_with_db(user_read_service):
    """
    Sincronizza la cache con il contenuto del database all'avvio del server.
    """
    try:
        # Recupera tutti gli utenti dal database
        rows=user_read_service.get_all_users_per_cache()
        with cache_lock:
            for row in rows:
                email,ticker,high_value,low_value=row
                requestEmail_cache[email] = {
                    "ticker": ticker,
                    "high_value": high_value,
                    "low_value": low_value
                }
        print("Cache sincronizzata con il database.")
        print(requestEmail_cache)
    except Error as e:
        print(f"Errore durante la sincronizzazione della cache con il database: {e}")

requestEmail_cache = {}
# A lock to synchronize access to the cache for thread safety
cache_lock = Lock()

# Funzione per validare l'email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Funzione per validare che high_value sia maggiore di low_value
def is_high_value_greater_than_low_value(high_value, low_value):
    return high_value > low_value if high_value is not None and low_value is not None else True

class UserService(protoBuffer_pb2_grpc.UserServiceServicer):
    def __init__(self,user_read_service,user_write_service,financial_read_service):
        self.user_read_service=user_read_service
        self.user_write_service=user_write_service
        self.financial_read_service=financial_read_service

    def Registrazione_utente(self,request,context):
        email=request.email
        ticker=request.ticker
        high_value=request.high_value.value if request.HasField("high_value") else None
        low_value=request.low_value.value if request.HasField("low_value") else None

        # Controllo email
        if not is_valid_email(email):
            response = protoBuffer_pb2.Registrazione_utente_Reply(messaggio="Email non valida",stato_registrazione="failed")
            return response

        #qui è implementato l'at most once
        with cache_lock:
            print("Cache content:\n")
            print(requestEmail_cache)
            if email in requestEmail_cache:
                print(f"l'utente con email {email} è gia registrato")
                response = protoBuffer_pb2.Registrazione_utente_Reply(messaggio="l'utente è gia registrato",stato_registrazione="failed")
                return response

        # Controllo che high_value sia maggiore di low_value
        if not is_high_value_greater_than_low_value(high_value, low_value):
            response = protoBuffer_pb2.Registrazione_utente_Reply(
                messaggio="high_value deve essere maggiore di low_value",
                stato_registrazione="failed"
            )
            return response

        print(f"registrazione utente con email: {email}")

        #registrazione nuovo utente
        print(f"sto processando una nuova richiesta con email={email}, ticker={ticker}")
        command=AddUserCommand(email,ticker,high_value,low_value)
        try:
            self.user_write_service.handle_add_user(command)
            response = protoBuffer_pb2.Registrazione_utente_Reply(messaggio="l'utente si è registrato con successo", stato_registrazione="success")
            with cache_lock:
                requestEmail_cache[email]={
                    "ticker":ticker,
                    "high_value":high_value,
                    "low_value":low_value
                }
                print(requestEmail_cache)        
            return response    
        except Error as e:
            print(f"errore durante la registrazione:{e}")
            response = protoBuffer_pb2.Registrazione_utente_Reply(messaggio="errore durante la registrazione", stato_registrazione="failed")
            return response
        
    def Aggiornamento_utente(self, request, context):
        email=request.email
        ticker=request.ticker
        high_value=request.high_value.value if request.HasField("high_value") else None
        low_value=request.low_value.value if request.HasField("low_value") else None

        # Controllo email
        if not is_valid_email(email):
            response = protoBuffer_pb2.Aggiornamento_utente_Reply(messaggio="Email non valida",stato_aggiornamento="failed")
            return response
        
        #qui è implementato l'at most once
        with cache_lock:
            if email in requestEmail_cache:
                cache_user=requestEmail_cache[email]
                #controllo se ticker è identico anche se le soglie sono diverse io non lo accetto perche c'è quella funzionalita apposita
                if cache_user["ticker"]==ticker:
                    print(f"la preferenza dell'utente: {email} non è cambiata")
                    print("quindi il contenuto della cache è:\n")
                    print(requestEmail_cache)
                    response = protoBuffer_pb2.Aggiornamento_utente_Reply(messaggio="il ticker non è cambiato",stato_aggiornamento="failed")
                    return response
            else:
                print("l'utente non è registrato")
                response = protoBuffer_pb2.Aggiornamento_utente_Reply(messaggio="utente non registrato",stato_aggiornamento="failed")
                return response        

        # Controllo che high_value sia maggiore di low_value
        if not is_high_value_greater_than_low_value(high_value, low_value):
            response = protoBuffer_pb2.Aggiornamento_utente_Reply(
                messaggio="high_value deve essere maggiore di low_value",
                stato_aggiornamento="failed"
            )
            return response
        
        #AGGIORNAMENTO TICKER DELL'UTENTE GIA ISCRITTO
        print(f"sto effettuando un aggiornamento del ticker, con email={email}, ticker={ticker}, high_value={high_value}, low_value={low_value}")
        command=UpdateUserCommand(email,ticker,high_value,low_value)
        try:
            self.user_write_service.handle_update_user(command)    
            response = protoBuffer_pb2.Aggiornamento_utente_Reply(messaggio="il ticker è stato aggiornato con successo", stato_aggiornamento="success")
            with cache_lock:
                requestEmail_cache[email]={
                    "ticker":ticker,
                    "high_value":high_value,
                    "low_value":low_value    
                }
                print(requestEmail_cache)        
            return response    
        except Error as e:
            print(f"errore durante l'aggiornamento':{e}")
            response = protoBuffer_pb2.Aggiornamento_utente_Reply(messaggio="errore durante l'aggiornamento'", stato_aggiornamento="failed")
            return response
        
    def Aggiornamento_Soglia(self, request, context):
        email=request.email
        ticker=request.ticker
        high_value=request.high_value.value if request.HasField("high_value") else None
        low_value=request.low_value.value if request.HasField("low_value") else None

        # Controllo email
        if not is_valid_email(email):
            response = protoBuffer_pb2.Aggiornamento_Soglia_Reply(messaggio="Email non valida",stato_aggiornamento="failed")
            return response

        #qui è implementato l'at most once
        with cache_lock:
            if email in requestEmail_cache:
                cache_user=requestEmail_cache[email]
                #confronto i valori nella cache
                if cache_user["ticker"] ==ticker:
                    if cache_user["high_value"]== high_value and cache_user["low_value"]== low_value:
                        print(f"le soglie dell'utente: {email} non sono cambiate")
                        response = protoBuffer_pb2.Aggiornamento_Soglia_Reply(messaggio="le soglie non sono cambiate",stato_aggiornamento="failed")
                        return response
                else:
                    response = protoBuffer_pb2.Aggiornamento_Soglia_Reply(messaggio="l'utente ha messo un ticker diverso",stato_aggiornamento="failed")
                    return response   
            else:
                response = protoBuffer_pb2.Aggiornamento_Soglia_Reply(messaggio="l'utente non è registrato",stato_aggiornamento="failed")
                return response

        # Controllo che high_value sia maggiore di low_value
        if not is_high_value_greater_than_low_value(high_value, low_value):
            response = protoBuffer_pb2.Aggiornamento_Soglia_Reply(
                messaggio="high_value deve essere maggiore di low_value",
                stato_aggiornamento="failed"
            )
            return response
        
        #AGGIORNAMENTO SOGLI*
        print(f"sto effettuando un aggiornamento della/e soglia/e con email={email}, ticker={ticker}, high_value={high_value}, low_value={low_value}")
        command=UpdateUserSogliaCommand(email,high_value,low_value)
        try:
            self.user_write_service.handle_update_soglia_user(command)
            response = protoBuffer_pb2.Aggiornamento_Soglia_Reply(messaggio="aggiornamento sogli* effettuato con successo", stato_aggiornamento="success")
            with cache_lock:
                requestEmail_cache[email]={
                    "ticker":ticker,
                    "high_value":high_value,
                    "low_value":low_value    
                }
                print(requestEmail_cache)        
            return response    
        except Error as e:
            print(f"errore durante l'aggiornamento':{e}")
            response = protoBuffer_pb2.Aggiornamento_Soglia_Reply(messaggio="errore durante l'aggiornamento'", stato_aggiornamento="failed")
            return response

    def Delete_utente(self, request, context):
        email=request.email
        with cache_lock:
            if email in requestEmail_cache:
                del requestEmail_cache[email]
                print(f"sto effettuando il delete dell'utente con email={email}")
                command=DeleteUserCommand(email)
                try:
                    self.user_write_service.handle_delete_user(command)
                    response = protoBuffer_pb2.Delete_utente_Reply(messaggio="l'utente è stato eliminato con successo", stato_delete="success")
                    return response    
                except Error as e:
                    print(f"errore durante l'eliminazione':{e}")
                    response = protoBuffer_pb2.Delete_utente_Reply(messaggio="errore durante l'eliminazione'", stato_delete="failed")
                    return response
            else:
                response = protoBuffer_pb2.Delete_utente_Reply(messaggio="l'utente non è registrato", stato_delete="failed")
                return response
    
    def Get_Last_Value(self, request, context):
        #recupero l'ultimo valore del ticker a cui l'utente è interessato
        email=request.email
        ticker=request.ticker
        try:
            result=self.financial_read_service.get_last_value(email,ticker)
            if result is None:
                print("non è presente nessun valore inerente a questi dati quindi:\n")
                return protoBuffer_pb2.Get_Last_Value_utente_Reply(res=-1) #ritorna -1 se nessun valore è stato trovato
            else:
                return protoBuffer_pb2.Get_Last_Value_utente_Reply(res=result[0])
        except Error as err:
            print(f"Errore durante la connessione al database:{err}")
            return protoBuffer_pb2.Get_Last_Value_utente_Reply(res=-1)  #Codice di errore
        
    def Get_Media(self, request, context):
        email=request.email
        ticker=request.ticker
        num_valori=request.num_valori
        try:
            count_result,result=self.financial_read_service.get_num_righe_AND_get_valor(email,ticker,num_valori)
            if count_result is None or count_result[0]==0:
                #non è stato trovato nessun valore inerente al ticker e alla mail
                print("il numero di valori presente per quel ticker è 0 \n")
                return protoBuffer_pb2.Get_Media_utente_Reply(media=-1)
            valori_tot=count_result[0]
            if num_valori> valori_tot:
                print(f"il numero di valori richiesto ({num_valori}) è maggiore dei valori disponibili ({valori_tot})")
                return protoBuffer_pb2.Get_Media_utente_Reply(media=-1)
            
            if result is None or len(result)==0:
                return protoBuffer_pb2.Get_Media_utente_Reply(media=-1) #ritorna -1 se nessun valore è stato trovato
            else:
                values=[row[0] for row in result]
                valore_media=sum(values)/num_valori
                return protoBuffer_pb2.Get_Media_utente_Reply(media=valore_media)
        except Error as err:
            print(f"Errore durante il calcolo della media:{err}")
            return protoBuffer_pb2.Get_Media_utente_Reply(media=-1)
        
def serve():
    user_read_service=UserReadService()
    # Sincronizzazione iniziale della cache con il database
    sync_cache_with_db(user_read_service)

    user_write_service=UserWriteService()
    financial_read_service=FinancialReadService()

    user_service=UserService(user_read_service,user_write_service,financial_read_service)

    port = '50051'
    # Initialize a thread pool with 10 workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Register the UserService with the server
    protoBuffer_pb2_grpc.add_UserServiceServicer_to_server(user_service, server)
    # Bind the server to the specified port
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("UserService started, listening on " + port)
    server.wait_for_termination()

if __name__=='__main__':
    serve()