import os
import itertools


def snap_dir(DIR):
    files_stat = {}
    for root, dirs, files in os.walk(DIR):
        for filename in files:
            try:
                abs_name = os.path.join(root, filename)
                file_stat = os.stat(abs_name)
                files_stat[abs_name] = (file_stat.st_mtime_ns, file_stat.st_size)
            except FileNotFoundError:
                continue
    return files_stat


def compare_dir_snaps(snap_before_sleep, snap_after_sleep):
    created = []
    modified = []
    deleted = []
    for a, b in itertools.zip_longest(snap_before_sleep, snap_after_sleep):
        if a == b:
            if snap_before_sleep[a][0] != snap_after_sleep[b][0]:
                modified.append((a, snap_before_sleep[a][1]))
                continue
        if a in snap_after_sleep:
            if snap_before_sleep[a][0] != snap_after_sleep[a][0]:
                modified.append((a, snap_after_sleep[a][1]))
        elif a is not None:
            deleted.append((a, snap_before_sleep[a][1]))
        if b in snap_before_sleep:
            if snap_before_sleep[b][0] != snap_after_sleep[b][0]:
                modified.append((b, snap_after_sleep[b][1]))
        elif b is not None:
            created.append((b, snap_after_sleep[b][1]))

    return created, deleted, modified
