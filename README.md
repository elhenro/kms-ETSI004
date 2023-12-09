# QKD Key Management Service Implementation

This project is a Python implementation of the ETSI004 standard, simulating the interface between a Quantum Key Distribution (QKD) Key Management Service (KMS) and a client application, using gRPC and protobuf.

## Setup

To run this project you can set up a virtual environment and install the required packages:

```
python -m venv kms-ETSI004-env
source kms-ETSI004-env/bin/activate
pip install -r requirements.txt
```

## Running the Application

To start the server, run:

```
python server/server.py
```

In a separate terminal, run the client example to make requests to the server:

```
python client/client.py
```

## Structure

The project includes the following components:

- `server/`: Contains the gRPC server implementation.
- `client/`: Contains the gRPC client implementation.
- `protos/`: Contains the Protocol Buffers definition file.
- `qkd_pb2.py` & `qkd_pb2_grpc.py`: Generated Python code from the Protocol Buffers definitions.