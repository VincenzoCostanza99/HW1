# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protoBuffer.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'protoBuffer.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11protoBuffer.proto\x12\x03HW1\"=\n\x1cRegistrazione_utente_Request\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\"L\n\x1aRegistrazione_utente_Reply\x12\x11\n\tmessaggio\x18\x01 \x01(\t\x12\x1b\n\x13stato_registrazione\x18\x02 \x01(\t\"=\n\x1c\x41ggiornamento_utente_Request\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\"L\n\x1a\x41ggiornamento_utente_Reply\x12\x11\n\tmessaggio\x18\x01 \x01(\t\x12\x1b\n\x13stato_aggiornamento\x18\x02 \x01(\t\"&\n\x15\x44\x65lete_utente_Request\x12\r\n\x05\x65mail\x18\x01 \x01(\t\">\n\x13\x44\x65lete_utente_Reply\x12\x11\n\tmessaggio\x18\x01 \x01(\t\x12\x14\n\x0cstato_delete\x18\x02 \x01(\t\">\n\x1dGet_Last_Value_utente_Request\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\"*\n\x1bGet_Last_Value_utente_Reply\x12\x0b\n\x03res\x18\x01 \x01(\x01\"M\n\x18Get_Media_utente_Request\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\x12\x12\n\nnum_valori\x18\x03 \x01(\x05\"\'\n\x16Get_Media_utente_Reply\x12\r\n\x05media\x18\x01 \x01(\x01\x32\xb7\x03\n\x0bUserService\x12\\\n\x14Registrazione_utente\x12!.HW1.Registrazione_utente_Request\x1a\x1f.HW1.Registrazione_utente_Reply\"\x00\x12\\\n\x14\x41ggiornamento_utente\x12!.HW1.Aggiornamento_utente_Request\x1a\x1f.HW1.Aggiornamento_utente_Reply\"\x00\x12G\n\rDelete_utente\x12\x1a.HW1.Delete_utente_Request\x1a\x18.HW1.Delete_utente_Reply\"\x00\x12X\n\x0eGet_Last_Value\x12\".HW1.Get_Last_Value_utente_Request\x1a .HW1.Get_Last_Value_utente_Reply\"\x00\x12I\n\tGet_Media\x12\x1d.HW1.Get_Media_utente_Request\x1a\x1b.HW1.Get_Media_utente_Reply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protoBuffer_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTRAZIONE_UTENTE_REQUEST']._serialized_start=26
  _globals['_REGISTRAZIONE_UTENTE_REQUEST']._serialized_end=87
  _globals['_REGISTRAZIONE_UTENTE_REPLY']._serialized_start=89
  _globals['_REGISTRAZIONE_UTENTE_REPLY']._serialized_end=165
  _globals['_AGGIORNAMENTO_UTENTE_REQUEST']._serialized_start=167
  _globals['_AGGIORNAMENTO_UTENTE_REQUEST']._serialized_end=228
  _globals['_AGGIORNAMENTO_UTENTE_REPLY']._serialized_start=230
  _globals['_AGGIORNAMENTO_UTENTE_REPLY']._serialized_end=306
  _globals['_DELETE_UTENTE_REQUEST']._serialized_start=308
  _globals['_DELETE_UTENTE_REQUEST']._serialized_end=346
  _globals['_DELETE_UTENTE_REPLY']._serialized_start=348
  _globals['_DELETE_UTENTE_REPLY']._serialized_end=410
  _globals['_GET_LAST_VALUE_UTENTE_REQUEST']._serialized_start=412
  _globals['_GET_LAST_VALUE_UTENTE_REQUEST']._serialized_end=474
  _globals['_GET_LAST_VALUE_UTENTE_REPLY']._serialized_start=476
  _globals['_GET_LAST_VALUE_UTENTE_REPLY']._serialized_end=518
  _globals['_GET_MEDIA_UTENTE_REQUEST']._serialized_start=520
  _globals['_GET_MEDIA_UTENTE_REQUEST']._serialized_end=597
  _globals['_GET_MEDIA_UTENTE_REPLY']._serialized_start=599
  _globals['_GET_MEDIA_UTENTE_REPLY']._serialized_end=638
  _globals['_USERSERVICE']._serialized_start=641
  _globals['_USERSERVICE']._serialized_end=1080
# @@protoc_insertion_point(module_scope)
