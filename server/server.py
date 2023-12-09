import sys
import os
import signal
from concurrent import futures
import grpc
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..') # todo package
import qkd_pb2
import qkd_pb2_grpc

class KeyManagementServicer(qkd_pb2_grpc.QKDKeyManagementServiceServicer):
    @staticmethod
    def validate_credentials(client_id, auth_token):
        # TODO actually validate client_id and auth_token
        return True

    @staticmethod
    def validate_session(session_token):
        # TODO validate session_token
        return True

    @staticmethod
    def retrieve_key_data(key_id):
        # TODO logic for retrieving key data
        return "dummy_key"

    @staticmethod
    def close_session(client_id, session_token):
        # TODO actually close the session
        return True

    def OpenConnect(self, request, context):
        if not request.client_id or not request.auth_token:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Client ID and Auth Token are required.')
            return qkd_pb2.OpenConnectResponse()
        if not self.validate_credentials(request.client_id, request.auth_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Invalid client ID or auth token.')
            return qkd_pb2.OpenConnectResponse()
        return qkd_pb2.OpenConnectResponse(success=True, message="Connection opened", session_token="dummy_token")

    def GetKey(self, request, context):
        if not request.session_token:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Session token is missing.')
            return qkd_pb2.GetKeyResponse()
        if not self.validate_session(request.session_token):
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Invalid session token.')
            return qkd_pb2.GetKeyResponse()
        key_data = self.retrieve_key_data(request.key_id)
        if key_data is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Key not found.')
            return qkd_pb2.GetKeyResponse()
        return qkd_pb2.GetKeyResponse(success=True, key_data=key_data, message="Key retrieved")

    def Close(self, request, context):
        if not request.client_id or not request.session_token:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Client ID and Session Token are required.')
            return qkd_pb2.CloseResponse()
        
        if not self.validate_session(request.session_token):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Session not found or already closed.')
            return qkd_pb2.CloseResponse()
        
        if not self.close_session(request.client_id, request.session_token):
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to close the session.')
            return qkd_pb2.CloseResponse()
        
        return qkd_pb2.CloseResponse(success=True, message="Connection closed")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    qkd_pb2_grpc.add_QKDKeyManagementServiceServicer_to_server(KeyManagementServicer(), server)

    # TODO for prod set up secure communication with TLS
    server.add_insecure_port('[::]:1337')
    server.start()

    def handle_sigterm(*args):
        print("Received shutdown signal")
        all_rpcs_done_event = server.stop(3)
        all_rpcs_done_event.wait(3)
        print("Server shut down gracefully")

    signal.signal(signal.SIGTERM, handle_sigterm)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        handle_sigterm()

if __name__ == '__main__':
    serve()