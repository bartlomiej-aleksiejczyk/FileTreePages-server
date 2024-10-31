import json
import os
from contextlib import contextmanager
from django.http import (
    Http404,
)
from django.conf import settings

if os.name == "posix":
    import fcntl

    @contextmanager
    def file_lock(file):
        fcntl.flock(file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(file, fcntl.LOCK_UN)

elif os.name == "nt":
    import msvcrt

    @contextmanager
    def file_lock(file):
        msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, os.path.getsize(file.name))
        try:
            yield
        finally:
            msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(file.name))


class JSONSaveError(Exception):
    """Custom exception for errors encountered while saving a JSON."""

    pass


def save_json(json_data, json_path):
    try:
        with open(json_path, "w", encoding="utf-8") as json_file:
            with file_lock(json_file):
                json.dump(json_data, json_file, indent=4)
    except (OSError, IOError) as e:
        raise JSONSaveError(f"Could not save JSON data: {e}") from e


def load_file_or_404(node_dir, file_name, error_message):
    file_path = os.path.join(node_dir, file_name)
    if not os.path.exists(file_path):
        raise Http404(error_message)
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_json_or_404(node_dir, file_name, error_message):
    file_path = os.path.join(node_dir, file_name)
    if not os.path.exists(file_path):
        raise Http404(error_message)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise Http404("Invalid JSON format in the file.")
