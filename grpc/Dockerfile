ARG BASE_IMAGE=python:3.12
FROM $BASE_IMAGE

COPY . .
WORKDIR .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/books.proto

EXPOSE 50051
ENTRYPOINT [ "python", "books_server.py" ]