from collections import Counter
from collections.abc import Iterable
from datetime import datetime
from functools import reduce
from itertools import groupby
from typing import Any


from src.models import RequestLogEntry


def count_status_codes(entries: Iterable[RequestLogEntry]) -> dict[int, int]:
    """Counts requests for each http status code"""

    return dict(Counter(entry.status for entry in entries))


def count_requests_by_ip(entries: Iterable[RequestLogEntry]) -> dict[str, int]:
    """Counts requests for each ip address"""

    return dict(Counter(entry.ip for entry in entries))


def find_top_urls(
    entries: Iterable[RequestLogEntry], limit: int = 3
) -> list[tuple[str, int]]:
    """Returns the most frequently accessed urls"""

    url_counts = Counter(entry.url for entry in entries)
    return url_counts.most_common(limit)


def calculate_total_bytes(entries: Iterable[RequestLogEntry]) -> int:
    """Calculates total response bytes"""

    return reduce(lambda total, entry: total + (entry.bytes or 0), entries, 0)


# TODO: Refactor needed
def group_entries_by_hour(entries: Iterable[RequestLogEntry]) -> dict[datetime, int]:
    """Counts requests grouped by hour"""

    sorted_entries = sorted(
        entries,
        key=lambda entry: entry.timestamp.replace(minute=0, second=0, microsecond=0),
    )

    hourly_counts = {}

    for hour, group in groupby(
        sorted_entries,
        key=lambda entry: entry.timestamp.replace(minute=0, second=0, microsecond=0),
    ):
        hourly_counts[hour] = sum(1 for _ in group)

    return hourly_counts


def generate_report(entries: Iterable[RequestLogEntry]) -> dict[str, Any]:
    """Generate a report containing the main statistics"""

    entries = list(entries)

    return {
        "total_requests": len(entries),
        "status_counts": count_status_codes(entries),
        "requests_by_ip": count_requests_by_ip(entries),
        "top_urls": find_top_urls(entries),
        "total_bytes": calculate_total_bytes(entries),
        "requests_by_hour": group_entries_by_hour(entries),
    }
