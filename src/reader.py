from pathlib import Path

from src.parser import parse_log_line


def read_log_lines(file_path: str | Path):
    """Yields lines from a log file."""

    with open(file_path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            yield line.strip("\n")


def iter_log_entries(file_path: str | Path):
    """Iterates over log entries"""

    for line in read_log_lines(file_path=file_path):
        entry = parse_log_line(line=line)

        if entry is not None:
            yield entry


def batch_entries(entries, batch_size=100):
    """Yields a fixed size batch of entries at a time"""

    batch = []

    for entry in entries:
        batch.append(entry)

        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch
