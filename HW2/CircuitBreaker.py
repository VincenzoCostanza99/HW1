import time
import threading


class circuit_breaker:
    def __init__(self, failure_threshold, recovery_timeout, expected_exception=Exception):
        self.failure_threshold = failure_threshold          
        self.recovery_timeout = recovery_timeout            
        self.expected_exception = expected_exception        
        self.failure_count = 0                              #questo corrisponde al counter per continui fallimenti che ovviamente inizializzo a 0
        self.last_failure_time = None                       #Timestamp of the last failure
        self.state = 'CLOSED'                               #inizalizzo lo stato iniziale del circuito a close
        self.lock = threading.Lock()                        #Lock to ensure thread-safe operations

    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == 'OPEN':
                if self._is_recovered_time_elapsed():    
                    self.state = 'HALF_OPEN'
                else:
                    # il circuito è aperto, chiamata negata
                    raise CircuitBreakerOpenException("Circuit is open. Call denied.")
            
            try:
                result = func(*args, **kwargs)
                #In caso di successo, ripristinare il circuito se in HALF_OPEN o mantenerlo chiuso
                self._reset()
                return result
            except self.expected_exception as e:
                #gestisco l'expected exception
                self._record_failure()
                raise e

    def _reset(self):
        """reset il failure count e chiudo il circuito"""
        self.failure_count=0
        self.state='CLOSED'

    def _record_failure(self):
        """Registra un errore e aggiorna lo stato se viene raggiunta la soglia di errore."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

    def _is_recovered_time_elapsed(self):      
        """Controlla se il timeout di ripristino è trascorso dall'ultimo errore.
        Return:
        -true se il recovery timeout è scaduto, falso altrimenti
        """   
        if self.last_failure_time is None:
            return False
        return time.time() - self.last_failure_time >= self.recovery_timeout

class CircuitBreakerOpenException(Exception):
    pass