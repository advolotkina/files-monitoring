#!/usr/bin/env python3
import argparse
import os
import time
import socket
import json
import sys
from dir_snapshot import snap_dir, compare_dir_snaps

MODIFIED = 0
CREATED = 1
DELETED = 2

message_buffer = []


def send_update(json_message):
    """
    Метод для передачи сообщений серверу.
    При возникновении ошибки соединения, неотправленные сообщения складываются в буффер.
    """
    global message_buffer
    if json_message is None:
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if message_buffer:
                json_message += message_buffer
            message_buffer.clear()

            s.connect((HOST, PORT))
            s.sendall(bytes(json.dumps(json_message), encoding='utf-8'))
    except ConnectionRefusedError as c:
        message_buffer += json_message
        print(c)
    except ConnectionError as c:
        message_buffer += json_message
        print(c)


def prepare_data(created, deleted, modified):
    """
    Метод для упаковки событий в удобный для передачи формат.
    :param snap_diff: Объект DirectorySnapshotDiff, содержащий в себе списки:
    files_created, files_modified, files_deleted
    :return: Список словарей. Каждый элемент представляет собой событие о файле.
    """
    json_message = []
    for file in sorted(created):
        json_message.append({
                'file_path': file[0],
                'event_type': CREATED,
                'file_size': file[1]
            })
    for file in sorted(deleted):
        json_message.append({
                'file_path': file[0],
                'event_type': DELETED,
                'file_size': file[1]
            })
    for file in sorted(modified):
        json_message.append({
                'file_path': file[0],
                'event_type': MODIFIED,
                'file_size': file[1]
            })

    if not json_message:
        return None

    return json_message


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', '-d',
                        help='Определяет директорию, файлы которой, необходимо отслеживать',
                        required=True)
    parser.add_argument('-host',
                        help='Определяет IP адрес сервера, на который необходимо посылать сообщения',
                        required=True)
    parser.add_argument('-port', '-p',
                        type=int,
                        help='Определяет порт сервера, на который необходимо посылать сообщения',
                        required=True)
    args = parser.parse_args()
    DIR = os.path.abspath(args.dir)
    HOST = args.host
    PORT = args.port

    if not (os.path.exists(DIR) and os.path.isdir(DIR)):
        print(f'{DIR} - по данному пути нет папки.')
        sys.exit(0)

    if not(os.access(DIR, os.R_OK)):
        print(f'У вас нет доступа для чтения папки {DIR}')
        sys.exit(0)

    snap_before_sleep = snap_dir(DIR)
    while True:
        time.sleep(2)
        try:
            snap_after_sleep = snap_dir(DIR)
            created, deleted, modified = compare_dir_snaps(snap_before_sleep, snap_after_sleep)
        except FileNotFoundError:
            print('Ваша папка была удалена')
            sys.exit(0)
        json_message = prepare_data(created, deleted, modified)
        send_update(json_message)
        snap_before_sleep = snap_after_sleep
