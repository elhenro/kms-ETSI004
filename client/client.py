import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import grpc
import qkd_pb2
import qkd_pb2_grpc

def open_connect(stub):
    response = stub.OpenConnect(qkd_pb2.OpenConnectRequest(client_id="123", auth_token="abc"))
    print("OpenConnect Response:", response)

def get_key(stub):
    response = stub.GetKey(qkd_pb2.GetKeyRequest(key_id="key123", session_token="token123"))
    print("GetKey Response:", response)

def close(stub):
    response = stub.Close(qkd_pb2.CloseRequest(client_id="123", session_token="token123"))
    print("Close Response:", response)

def run():
    with grpc.insecure_channel('localhost:1337') as channel:
        stub = qkd_pb2_grpc.QKDKeyManagementServiceStub(channel)
        open_connect(stub)
        get_key(stub)
        close(stub)

if __name__ == '__main__':
    run()
