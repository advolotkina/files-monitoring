#!/usr/bin/env python3.8
import argparse
import datetime
import socket
import json
import threading
import jsonschema

HOST = '127.0.0.2'
PORT = 8888

events = {0: 'MODIFIED', 1: 'CREATED', 2: 'DELETED'}

message_schema = {
    "type": "array",
    "items": [{
        "type": "object",
        "required": ["file_path", "event_type", "file_size"],
        "properties": {
            "file_path": {"type": "string"},
            "event_type": {"type": "integer"},
            "file_size": {"type": "string"}
        }
    }
    ]
}


def deserialize_message(client_message):
    """
    Метод, десериализующий сообщение клиента.
    :param client_message: Bytearray object, который необходимо десериализовать в список объектов
    :return: None если сообщение клиента не является валидным json. Инача возвращается список объектов словаря.
    """
    try:
        json_message = json.loads(str(client_message[0:-1], encoding='utf-8'))
    except json.JSONDecodeError:
        return None
    try:
        jsonschema.validate(instance=json_message, schema=message_schema)
    except jsonschema.exceptions.ValidationError:
        return None
    return json_message


def serve_client_connection(conn):
    """
    Метод для обслуживания клиента.
    Считывает данные из сокета и выводит в консоль сообщения клиента.
    :param conn: Объект сокета.
    :return:
    """
    client_message = read_message(conn)
    if client_message is None:
        return

    messages = deserialize_message(client_message)
    if messages is None:
        return

    for message in messages:
        print(f"{datetime.datetime.now()} | "
              f"{message['file_path']:50} | "
              f"{message['file_size']:10} | "
              f"{events[message['event_type']]}")


def read_message(conn, delimiter=b'!'):
    """
    Данный метод считывает данные из сокета.
    :param conn: Объект сокета, из которого необходимо считать данные.
    :param delimiter: Последний символ в каждом сообщении клиента.
    :return: Возвращает None, если соедниние было прервано или сообщение клиента в виде bytearray в случае удачной
    передачи.
    """
    request = bytearray()
    try:
        with conn:
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    return None
                request += chunk
                if delimiter in request:
                    return request
    except ConnectionResetError:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='Определяет IP адрес данного сервера, по умолчанию - 127.0.0.2', default=HOST)
    parser.add_argument('-port', type=int, help='Определяет порт данного сервера, по умолчанию - 8888', default=PORT)
    args = parser.parse_args()
    if args.host:
        HOST = args.host
    if args.port:
        PORT = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            new_client = threading.Thread(target=serve_client_connection, args=(conn,))
            new_client.start()
