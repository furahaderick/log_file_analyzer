# flake8: noqa: E501
# pylint: disable=line-too-long

from datetime import datetime

from src.parser import parse_log_line


def test_parser_returns_none_on_invalid_line():
    invalid_line_parse = parse_log_line(
        '192.168.1.999 - - [32/Oct/2026:25:61:99 +9999] "GET /index.html HTTP/9.9" XYZ abc "-" "Mozilla/5.0"'
    )

    assert invalid_line_parse is None


def test_parser_successfully_parses_log_line():
    log_entry = parse_log_line(
        '192.168.1.10 - - [21/Oct/2026:12:50:00 +0200] "GET /index.html HTTP/1.1" 200 512'
    )
    assert log_entry is not None
    assert log_entry.ip == "192.168.1.10"
    assert log_entry.timestamp == datetime.strptime(
        "21/Oct/2026:12:50:00 +0200", "%d/%b/%Y:%H:%M:%S %z"
    )
    assert log_entry.method == "GET"
    assert log_entry.url == "/index.html"
    assert log_entry.status == 200
    assert log_entry.bytes == 512


def test_parser_gives_none_to_requests_without_size():
    log_entry = parse_log_line(
        '10.0.0.8 - - [21/Oct/2026:12:54:00 +0200] "GET /download HTTP/1.1" 200 -'
    )

    assert log_entry is not None
    assert log_entry.bytes is None
