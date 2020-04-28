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


def send_update(snap_diff):
    json_message = []
    if snap_diff.files_created:
        for file in snap_diff.files_created:
            json_message.append({
                'file_path': file,
                'event_type': CREATED,
                'file_size': os.stat(file).st_size
            })

    if snap_diff.files_modified:
        for file in snap_diff.files_modified:
            json_message.append({
                'file_path': file,
                'event_type': MODIFIED,
                'file_size': os.stat(file).st_size
            })

    if snap_diff.files_deleted:
        for file in snap_diff.files_deleted:
            json_message.append({
                'file_path': file,
                'event_type': DELETED,
                'file_size': ''
            })

    if not json_message:
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes(json.dumps(json_message) + '!', encoding='utf-8'))
    except ConnectionRefusedError:
        print('Connection refused')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', type=str, help='Определяет директорию, файлы которой, необходимо отслеживать')
    parser.add_argument('-host', help='Определяет IP адрес сервера, на который необходимо посылать сообщения')
    parser.add_argument('-port', help='Определяет порт сервера, на который необходимо посылать сообщения')
    args = parser.parse_args()
    DIR = args.dir
    HOST = args.host
    PORT = int(args.port)

    if not (os.path.exists(DIR) and os.path.isdir(DIR)):
        print(f'{DIR} - по данному пути нет папки.')
        sys.exit(0)

    while True:
        snap_before_sleep = DirectorySnapshot(DIR, True)
        time.sleep(2)
        snap_after_sleep = DirectorySnapshot(DIR, True)
        diff_snap = DirectorySnapshotDiff(snap_before_sleep, snap_after_sleep)
        send_update(diff_snap)
