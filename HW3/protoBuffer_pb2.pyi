from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Registrazione_utente_Request(_message.Message):
    __slots__ = ("email", "ticker", "high_value", "low_value")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    HIGH_VALUE_FIELD_NUMBER: _ClassVar[int]
    LOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    high_value: _wrappers_pb2.DoubleValue
    low_value: _wrappers_pb2.DoubleValue
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ..., high_value: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., low_value: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ...) -> None: ...

class Registrazione_utente_Reply(_message.Message):
    __slots__ = ("messaggio", "stato_registrazione")
    MESSAGGIO_FIELD_NUMBER: _ClassVar[int]
    STATO_REGISTRAZIONE_FIELD_NUMBER: _ClassVar[int]
    messaggio: str
    stato_registrazione: str
    def __init__(self, messaggio: _Optional[str] = ..., stato_registrazione: _Optional[str] = ...) -> None: ...

class Aggiornamento_utente_Request(_message.Message):
    __slots__ = ("email", "ticker", "high_value", "low_value")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    HIGH_VALUE_FIELD_NUMBER: _ClassVar[int]
    LOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    high_value: _wrappers_pb2.DoubleValue
    low_value: _wrappers_pb2.DoubleValue
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ..., high_value: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., low_value: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ...) -> None: ...

class Aggiornamento_utente_Reply(_message.Message):
    __slots__ = ("messaggio", "stato_aggiornamento")
    MESSAGGIO_FIELD_NUMBER: _ClassVar[int]
    STATO_AGGIORNAMENTO_FIELD_NUMBER: _ClassVar[int]
    messaggio: str
    stato_aggiornamento: str
    def __init__(self, messaggio: _Optional[str] = ..., stato_aggiornamento: _Optional[str] = ...) -> None: ...

class Aggiornamento_Soglia_Request(_message.Message):
    __slots__ = ("email", "ticker", "high_value", "low_value")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    HIGH_VALUE_FIELD_NUMBER: _ClassVar[int]
    LOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    high_value: _wrappers_pb2.DoubleValue
    low_value: _wrappers_pb2.DoubleValue
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ..., high_value: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., low_value: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ...) -> None: ...

class Aggiornamento_Soglia_Reply(_message.Message):
    __slots__ = ("messaggio", "stato_aggiornamento")
    MESSAGGIO_FIELD_NUMBER: _ClassVar[int]
    STATO_AGGIORNAMENTO_FIELD_NUMBER: _ClassVar[int]
    messaggio: str
    stato_aggiornamento: str
    def __init__(self, messaggio: _Optional[str] = ..., stato_aggiornamento: _Optional[str] = ...) -> None: ...

class Delete_utente_Request(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class Delete_utente_Reply(_message.Message):
    __slots__ = ("messaggio", "stato_delete")
    MESSAGGIO_FIELD_NUMBER: _ClassVar[int]
    STATO_DELETE_FIELD_NUMBER: _ClassVar[int]
    messaggio: str
    stato_delete: str
    def __init__(self, messaggio: _Optional[str] = ..., stato_delete: _Optional[str] = ...) -> None: ...

class Get_Last_Value_utente_Request(_message.Message):
    __slots__ = ("email", "ticker")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ...) -> None: ...

class Get_Last_Value_utente_Reply(_message.Message):
    __slots__ = ("res",)
    RES_FIELD_NUMBER: _ClassVar[int]
    res: float
    def __init__(self, res: _Optional[float] = ...) -> None: ...

class Get_Media_utente_Request(_message.Message):
    __slots__ = ("email", "ticker", "num_valori")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    NUM_VALORI_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    num_valori: int
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ..., num_valori: _Optional[int] = ...) -> None: ...

class Get_Media_utente_Reply(_message.Message):
    __slots__ = ("media",)
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    media: float
    def __init__(self, media: _Optional[float] = ...) -> None: ...
