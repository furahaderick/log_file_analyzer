from collections.abc import Iterable, Iterator
from dataclasses import replace
from datetime import datetime
from functools import partial
from itertools import chain, islice, takewhile

from src.models import RequestLogEntry


def transform_entry(entry: RequestLogEntry) -> RequestLogEntry:
    """Normalizes entries"""

    return replace(entry, method=entry.method.upper(), url=entry.url.strip())


def filter_by_status(
    entries: Iterable[RequestLogEntry], status_code: int
) -> Iterator[RequestLogEntry]:
    """Returns entries matching a specific status code"""

    return filter(lambda entry: entry.status == status_code, entries)


def filter_by_ip(
    entries: Iterable[RequestLogEntry], ip_address: str
) -> Iterator[RequestLogEntry]:
    """Returns entries matching a specific ip address"""

    return filter(lambda entry: entry.ip == ip_address, entries)


def filter_by_time_range(
    entries: Iterable[RequestLogEntry], start_time: datetime, end_time: datetime
) -> Iterator[RequestLogEntry]:
    """Returns entries matching a specific time range"""

    return filter(lambda entry: start_time <= entry.timestamp <= end_time, entries)


# Specialized filters
filter_not_found = partial(filter_by_status, status_code=404)
filter_server_error = partial(filter_by_status, status_code=500)


def combine_entries(
    *entry_sources: Iterable[RequestLogEntry],
) -> Iterator[RequestLogEntry]:
    """Combine multiple entry files into one run"""

    return chain.from_iterable(entry_sources)


def limit_entries(
    entries: Iterable[RequestLogEntry], limit: int
) -> Iterator[RequestLogEntry]:
    """Return at most the first 'limit' entries"""

    if limit < 0:
        raise ValueError("limit must be non-negative")

    return islice(entries, limit)


def take_entries_until(
    entries: Iterable[RequestLogEntry], end_time: datetime
) -> Iterator[RequestLogEntry]:
    """Takes entries until the end_time"""

    return takewhile(lambda entry: entry.timestamp <= end_time, entries)


def build_pipeline(
    entries: Iterable[RequestLogEntry],
    status_code: int | None = None,
    ip_address: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> Iterator[RequestLogEntry]:
    """Combines transformation and filtering"""

    # 1. transform
    pipeline = map(transform_entry, entries)

    # 2. apply filters if specified
    if status_code is not None:
        pipeline = filter_by_status(pipeline, status_code=status_code)

    if ip_address is not None:
        pipeline = filter_by_ip(pipeline, ip_address=ip_address)

    if start_time is not None and end_time is not None:
        pipeline = filter_by_time_range(
            pipeline, start_time=start_time, end_time=end_time
        )

    return pipeline
