import os

import smtplib
import ssl
import functools
from pathlib import Path
import argparse
import json5

from log import log

def catch_sending_errors(func):
    """Decorator that wraps a function to catch and log any exceptions during execution.

    Intended for use with email-sending functions to log errors per recipient.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            email = args[0]["To"]
            log.error(f"Error sending to '{email}': {e}")
    return wrapper


def is_inside_dir(file_path, directory_path):
    try:
        return Path(file_path).resolve().is_relative_to(Path(directory_path).resolve())
    except AttributeError:
        # For Python < 3.9
        try:
            Path(file_path).resolve().relative_to(Path(directory_path).resolve())
            return True
        except ValueError:
            return False

@catch_sending_errors
def send_email(msg, login, password, smtp_server = "smtp.gmail.com") -> None:
    with smtplib.SMTP_SSL(smtp_server, 465, context=ssl.create_default_context()) as server:
        server.login(login, password)
        server.send_message(msg=msg)


def normalize_name(file_path):
    name = os.path.splitext(os.path.basename(file_path))[0]
    return name.lower().replace(" ", "_")


def load_paths_from_dir(root_dir: str, file_extension : str | None = None) -> list[str]:
    """
    Recursively loads file paths from a directory, optionally filtered by file extension.

    Args:
        root_dir (str): Root directory to search in.
        file_extension (str, optional): File extension to filter by (e.g., '.pdf').

    Returns:
        List[str]: List of matching file paths.
    """
    paths: list[str] = []

    for dirpath, _, filenames in os.walk(root_dir):
        log.debug(f"Visiting: '{dirpath}'")
        for filename in filenames:
            if file_extension and not filename.lower().endswith(file_extension.lower()):
                continue

            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                log.debug(f"Adding '{file_path}' to the paths list.")
                paths.append(file_path)

    return paths


def load_str_list(filepath: str, label: str = "file") -> list:
    """
    Loads a list of strings from a .txt file, one per line.
    Logs the process and handles errors gracefully.

    Args:
        filepath (str): Path to the .txt file.
        label (str): Descriptive label used in logging.

    Returns:
        list[str]: List of lines (stripped) from the file.
    """
    try:
        log.debug(f"Opening {label} at: '{filepath}'.")
        with open(filepath, "r") as f:
            return [line.strip() for line in f]
    except Exception as e:
        log.error(f"Cannot open {label}: {e}")
        return []


def save_str_list(str_list: list, filepath: str, label: str = "file", mode='w') -> None:
    try:
        with open(filepath, mode) as f:
            for email in str_list:
                f.write(f"{email}\n")
        log.info(f"Saved {len(str_list)} items to '{label}' at: '{filepath}'.")
    except Exception as e:
        log.error(f"Failed to save {label}: {e}")


def parse_duration(duration_str: str) -> int:
    """
    Parses a human-readable duration string like "1h 30m" into seconds.
    """
    units = {'h': 3600, 'm': 60, 's': 1}
    total_seconds = 0
    for part in duration_str.lower().split():
        for unit in units:
            if part.endswith(unit):
                try:
                    total_seconds += int(part[:-1]) * units[unit]
                except ValueError:
                    raise argparse.ArgumentTypeError(f"Invalid duration: '{part}'")
                break
        else:
            raise argparse.ArgumentTypeError(f"Unknown duration unit in '{part}'")
    return total_seconds


def save_email_bool_map(email_bool_map: dict, filepath: str, label: str = "email bool map") -> None:
    """
    Saves a dictionary of email validation results to a JSON5 file.

    Args:
        email_bool_map (dict): Dictionary mapping emails to bool (valid/invalid).
        filepath (str): Path to save the JSON5 file.
        label (str): Optional label for logging purposes.
    """
    try:
        with open(filepath, "w") as f:
            json5.dump(email_bool_map, f, indent=2)
        log.info(f"Saved {len(email_bool_map)} entries to {label} at '{filepath}'.")
    except Exception as e:
        log.error(f"Failed to save {label} to '{filepath}': {e}")