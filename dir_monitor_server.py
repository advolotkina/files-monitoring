#!/usr/bin/env python3.8
import argparse
import datetime
import socket
import json
import threading

events = {0: 'MODIFIED', 1: 'CREATED', 2: 'DELETED'}
HOST = '127.0.0.2'
PORT = 8888


def serve_client_connection(conn):
    client_message = read_message(conn)
    if client_message is None:
        return

    json_message = json.loads(str(client_message[0:-1], encoding='utf-8'))
    for message in json_message:
        print(f"{datetime.datetime.now()} "
              f"{message['file_path']} "
              f"{message['file_size']} "
              f"{events[message['event_type']]}")


def read_message(conn, delimiter=b'!'):
    request = bytearray()
    try:
        with conn:
            while True:
                chunk = conn.recv(4)
                if not chunk:
                    return None
                request += chunk
                if delimiter in request:
                    return request
    except ConnectionResetError:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host')
    parser.add_argument('-port')
    args = parser.parse_args()
    # PORT = int(args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            new_client = threading.Thread(target=serve_client_connection, args=(conn,))
            new_client.start()

