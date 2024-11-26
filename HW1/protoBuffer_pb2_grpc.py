# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import protoBuffer_pb2 as protoBuffer__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in protoBuffer_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class UserServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Registrazione_utente = channel.unary_unary(
                '/HW1.UserService/Registrazione_utente',
                request_serializer=protoBuffer__pb2.Registrazione_utente_Request.SerializeToString,
                response_deserializer=protoBuffer__pb2.Registrazione_utente_Reply.FromString,
                _registered_method=True)
        self.Aggiornamento_utente = channel.unary_unary(
                '/HW1.UserService/Aggiornamento_utente',
                request_serializer=protoBuffer__pb2.Aggiornamento_utente_Request.SerializeToString,
                response_deserializer=protoBuffer__pb2.Aggiornamento_utente_Reply.FromString,
                _registered_method=True)
        self.Delete_utente = channel.unary_unary(
                '/HW1.UserService/Delete_utente',
                request_serializer=protoBuffer__pb2.Delete_utente_Request.SerializeToString,
                response_deserializer=protoBuffer__pb2.Delete_utente_Reply.FromString,
                _registered_method=True)
        self.Get_Last_Value = channel.unary_unary(
                '/HW1.UserService/Get_Last_Value',
                request_serializer=protoBuffer__pb2.Get_Last_Value_utente_Request.SerializeToString,
                response_deserializer=protoBuffer__pb2.Get_Last_Value_utente_Reply.FromString,
                _registered_method=True)
        self.Get_Media = channel.unary_unary(
                '/HW1.UserService/Get_Media',
                request_serializer=protoBuffer__pb2.Get_Media_utente_Request.SerializeToString,
                response_deserializer=protoBuffer__pb2.Get_Media_utente_Reply.FromString,
                _registered_method=True)


class UserServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Registrazione_utente(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Aggiornamento_utente(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete_utente(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_Last_Value(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_Media(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Registrazione_utente': grpc.unary_unary_rpc_method_handler(
                    servicer.Registrazione_utente,
                    request_deserializer=protoBuffer__pb2.Registrazione_utente_Request.FromString,
                    response_serializer=protoBuffer__pb2.Registrazione_utente_Reply.SerializeToString,
            ),
            'Aggiornamento_utente': grpc.unary_unary_rpc_method_handler(
                    servicer.Aggiornamento_utente,
                    request_deserializer=protoBuffer__pb2.Aggiornamento_utente_Request.FromString,
                    response_serializer=protoBuffer__pb2.Aggiornamento_utente_Reply.SerializeToString,
            ),
            'Delete_utente': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete_utente,
                    request_deserializer=protoBuffer__pb2.Delete_utente_Request.FromString,
                    response_serializer=protoBuffer__pb2.Delete_utente_Reply.SerializeToString,
            ),
            'Get_Last_Value': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_Last_Value,
                    request_deserializer=protoBuffer__pb2.Get_Last_Value_utente_Request.FromString,
                    response_serializer=protoBuffer__pb2.Get_Last_Value_utente_Reply.SerializeToString,
            ),
            'Get_Media': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_Media,
                    request_deserializer=protoBuffer__pb2.Get_Media_utente_Request.FromString,
                    response_serializer=protoBuffer__pb2.Get_Media_utente_Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'HW1.UserService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('HW1.UserService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class UserService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Registrazione_utente(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HW1.UserService/Registrazione_utente',
            protoBuffer__pb2.Registrazione_utente_Request.SerializeToString,
            protoBuffer__pb2.Registrazione_utente_Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Aggiornamento_utente(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HW1.UserService/Aggiornamento_utente',
            protoBuffer__pb2.Aggiornamento_utente_Request.SerializeToString,
            protoBuffer__pb2.Aggiornamento_utente_Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Delete_utente(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HW1.UserService/Delete_utente',
            protoBuffer__pb2.Delete_utente_Request.SerializeToString,
            protoBuffer__pb2.Delete_utente_Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Get_Last_Value(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HW1.UserService/Get_Last_Value',
            protoBuffer__pb2.Get_Last_Value_utente_Request.SerializeToString,
            protoBuffer__pb2.Get_Last_Value_utente_Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Get_Media(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HW1.UserService/Get_Media',
            protoBuffer__pb2.Get_Media_utente_Request.SerializeToString,
            protoBuffer__pb2.Get_Media_utente_Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
