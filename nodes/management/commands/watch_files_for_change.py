import os
import json
from datetime import datetime
from difflib import unified_diff
from django.core.management.base import BaseCommand
from django.conf import settings

# TODO: Switch to diff base storage, do not store entre content each change

try:
    import fcntl  # Unix-based locking
except ImportError:
    fcntl = None

try:
    import msvcrt  # Windows-based locking
except ImportError:
    msvcrt = None

os.umask(777)


def get_file_content(filepath):
    """Read and return content of a file."""
    with open(filepath, "r") as file:
        return file.readlines()


def lock_file(file):
    """Lock a file for exclusive access."""
    if fcntl:
        fcntl.flock(file, fcntl.LOCK_EX)
    elif msvcrt:
        msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, os.path.getsize(file.name))


def unlock_file(file):
    """Unlock a file."""
    if fcntl:
        fcntl.flock(file, fcntl.LOCK_UN)
    elif msvcrt:
        msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(file.name))


def add_entry_to_history(content, history_path):
    """Append entry with timestamp to history.json file."""
    with open(history_path, "r+") as history_file:
        try:
            lock_file(history_file)
            history = json.load(history_file)
            timestamp = datetime.now().isoformat()
            history.append({"timestamp": timestamp, "content": content})
            history_file.seek(0)
            json.dump(history, history_file, indent=4)
            history_file.truncate()
        finally:
            unlock_file(history_file)


def check_and_update_history(main_file, history_path):
    """Check if history.json reflects main.* content and update if not."""
    current_content = get_file_content(main_file)

    with open(history_path, "r") as history_file:
        history = json.load(history_file)
        baseline_content = history[-1] if history else {"content": ""}

    if baseline_content.get("content") != current_content:
        add_entry_to_history(current_content, history_path)


def traverse_and_check(root_dir):
    """Traverse directories recursively and check for main.* and history.json."""
    for dirpath, _, filenames in os.walk(root_dir):
        main_files = [f for f in filenames if f.startswith("main.")]
        if not main_files:
            continue

        main_file_path = os.path.join(dirpath, main_files[0])
        history_path = os.path.join(dirpath, "history.json")

        if not os.path.exists(history_path):
            with open(history_path, "w") as history_file:
                json.dump([], history_file)

        try:
            check_and_update_history(main_file_path, history_path)
        except Exception as e:
            print(f"Error processing {main_file_path}: {e}")
            continue


class Command(BaseCommand):
    help = "Watch node files and write history"

    def handle(self, *args, **kwargs):
        traverse_and_check(settings.PAGES_BASE_DIR)
