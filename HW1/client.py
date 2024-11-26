import grpc
import protoBuffer_pb2
import protoBuffer_pb2_grpc


def run():
    # Set the target server address
    target = 'localhost:50051'

    # Establish a connection to the gRPC server
    with grpc.insecure_channel(target) as channel:
        # Create a stub (client) for the UserService
        stub = protoBuffer_pb2_grpc.UserServiceStub(channel)

        while True:
            print("seleziona la funzionalità che vuoi usare:")
            print("1:registrazione utente")
            print("2:aggiornamento utente")
            print("3:cancellazione utente")
            print("4: restituisce l'ultimo valore del ticker")
            print("5: restituisce la media degli ultimi N valori del ticker")
            print("0:esci")
            scelta=input("scelta: ")

            if scelta=='1':
                email=input("inserisci la tua email: ")
                ticker=input("inserisci il tuo ticker: ")
                #creo la richiesta con email e ticker
                request= protoBuffer_pb2.Registrazione_utente_Request(email=email,ticker=ticker)
                try:
                    response= stub.Registrazione_utente(request)
                    #risposta da parte del server
                    print(f"Risposta del server:{response.messaggio}, Stato:{response.stato_registrazione}")
                except grpc.RpcError as e:
                    print(f"RPC failed with code {e.code()}: {e.details()}")
            elif scelta=='2':
                email=input("inserisci l'email esistente: ")
                ticker=input("inserisci il nuovo ticker: ")
                #creo la richiesta con email e ticker
                request=protoBuffer_pb2.Aggiornamento_utente_Request(email=email,ticker=ticker)
                try:
                    response= stub.Aggiornamento_utente(request)
                    #risposta da parte del server
                    print(f"Risposta del server:{response.messaggio}, Stato:{response.stato_aggiornamento}")
                except grpc.RpcError as e:
                    print(f"RPC failed with code {e.code()}: {e.details()}")
            elif scelta=='3':
                email=input("inserisci l'email da eliminare: ")
                #creo la richiesta con email e ticker
                request=protoBuffer_pb2.Delete_utente_Request(email=email)
                try:
                    response= stub.Delete_utente(request)
                    #risposta da parte del server
                    print(f"Risposta del server:{response.messaggio}, Stato:{response.stato_delete}")
                except grpc.RpcError as e:
                    print(f"RPC failed with code {e.code()}: {e.details()}")
            elif scelta=='4':
                email=input("inserisci l'email: ")
                ticker=input("inserisci il ticker: ")
                #creo la richiesta con email e ticker
                request=protoBuffer_pb2.Get_Last_Value_utente_Request(email=email,ticker=ticker)
                try:
                    response= stub.Get_Last_Value(request)
                    #risposta da parte del server
                    print(f"l'ultimo valore del ticker {ticker} è:{response.res}")
                except grpc.RpcError as e:
                    print(f"RPC failed with code {e.code()}: {e.details()}") 
            elif scelta=='5':
                email=input("inserisci l'email: ")
                ticker=input("inserisci il ticker: ")
                num_valori=int(input("inserisci il numero di valori piu recenti per il quale fare la media: "))
                #creo la richiesta con email, ticker e num_valori
                request=protoBuffer_pb2.Get_Media_utente_Request(email=email,ticker=ticker,num_valori=num_valori)
                try:
                    response= stub.Get_Media(request)
                    #risposta da parte del server
                    print(f"la media degli ultimi {num_valori} valori del ticker{ticker} è: {response.media}")
                except grpc.RpcError as e:
                    print(f"RPC failed with code {e.code()}: {e.details()}")
            elif scelta=='0':
                print("USCITA DAL PROGRAMMA")
                break
            else:
                print("scelta non valida riprova")


if __name__ == '__main__':
    run()