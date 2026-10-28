# pylint: disable=redefined-outer-name

from datetime import UTC, datetime, timedelta

import pytest

from src.models import RequestLogEntry


@pytest.fixture
def sample_log_line():
    return (
        "192.168.1.10 - - [22/Oct/2026:19:03:36 +0200] "
        '"GET /products HTTP/1.1" 200 1234'
    )


@pytest.fixture
def sample_log_lines():
    return [
        '192.168.1.10 - - [22/Oct/2026:19:00:00 +0200] "GET / HTTP/1.1" 200 100',
        '192.168.1.11 - - [22/Oct/2026:19:01:00 +0200] "POST /login HTTP/1.1" 201 200',
        '192.168.1.10 - - [22/Oct/2026:19:02:00 +0200] "GET /missing HTTP/1.1" 404 50',
        '192.168.1.12 - - [22/Oct/2026:20:00:00 +0200] "DELETE /products/1 HTTP/1.1" 500 0',
    ]


@pytest.fixture
def sample_entries():
    timestamp = datetime(2026, 10, 22, 19, 0, tzinfo=UTC)

    return [
        RequestLogEntry(
            ip="192.168.1.10",
            timestamp=timestamp,
            method="GET",
            url="/",
            status=200,
            bytes=100,
        ),
        RequestLogEntry(
            ip="192.168.1.11",
            timestamp=timestamp + timedelta(minutes=1),
            method="POST",
            url="/login",
            status=201,
            bytes=200,
        ),
        RequestLogEntry(
            ip="192.168.1.10",
            timestamp=timestamp + timedelta(minutes=2),
            method="GET",
            url="/missing",
            status=404,
            bytes=50,
        ),
        RequestLogEntry(
            ip="192.168.1.12",
            timestamp=timestamp + timedelta(hours=1),
            method="DELETE",
            url="/products/1",
            status=500,
            bytes=0,
        ),
    ]


@pytest.fixture
def sample_entries_same_hour(sample_entries):
    """Entries used to test hourly grouping."""
    return sample_entries[:3]
