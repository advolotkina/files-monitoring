#!/usr/bin/env python3.8
import argparse
import os
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
import time
import socket
import json
import sys

MODIFIED = 0
CREATED = 1
DELETED = 2

message_buffer = []


def send_update(snap_diff, stat_info):
    """
    Метод для передачи сообщений серверу.
    При возникновении ошибки соединения, неотправленные сообщения складываются в буффер.
    """
    json_message = prepare_data(snap_diff, stat_info)
    global message_buffer
    if json_message is None:
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if message_buffer:
                json_message += message_buffer
            message_buffer.clear()

            s.connect((HOST, PORT))
            s.sendall(bytes(json.dumps(json_message) + '/', encoding='utf-8'))
    except ConnectionRefusedError as c:
        message_buffer += json_message
        print(c)
    except ConnectionError as c:
        message_buffer += json_message
        print(c)


def prepare_data(snap_diff, stat_info):
    """
    Метод для упаковки событий в удобный для передачи формат.
    :param snap_diff: Объект DirectorySnapshotDiff, содержащий в себе списки:
    files_created, files_modified, files_deleted
    :return: Список словарей. Каждый элемент представляет собой событие о файле.
    """
    json_message = []
    if snap_diff.files_created:
        for file in snap_diff.files_created:
            json_message.append({
                'file_path': file,
                'event_type': CREATED,
                'file_size': stat_info[file].st_size
            })
    if snap_diff.files_modified:
        for file in snap_diff.files_modified:
            json_message.append({
                'file_path': file,
                'event_type': MODIFIED,
                'file_size': stat_info[file].st_size
            })

    if snap_diff.files_deleted:
        for file in snap_diff.files_deleted:
            json_message.append({
                'file_path': file,
                'event_type': DELETED,
                'file_size': -1
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

    snap_before_sleep = DirectorySnapshot(DIR, True)
    while True:
        time.sleep(2)
        try:
            snap_after_sleep = DirectorySnapshot(DIR, True)
            diff_snap = DirectorySnapshotDiff(snap_before_sleep, snap_after_sleep)
        except FileNotFoundError:
            print('Ваша папка была удалена')
            sys.exit(0)
        send_update(diff_snap, snap_after_sleep._stat_info)
        snap_before_sleep = snap_after_sleep
