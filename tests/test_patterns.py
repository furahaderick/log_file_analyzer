import re

from src.patterns import log_line_pattern


def test_log_line_pattern_is_compiled():
    assert isinstance(log_line_pattern, re.Pattern)


def test_matches_valid_get_request(sample_log_line):
    assert log_line_pattern.fullmatch(sample_log_line) is not None


def test_matches_different_http_method():
    line = (
        "10.0.0.1 - - [22/Oct/2026:19:03:36 +0200] " '"DELETE /items/1 HTTP/1.1" 204 0'
    )
    assert log_line_pattern.fullmatch(line) is not None


def test_matches_query_string_url():
    line = (
        "10.0.0.1 - - [22/Oct/2026:19:03:36 +0200] "
        '"GET /search?q=python HTTP/1.1" 200 120'
    )
    assert log_line_pattern.fullmatch(line) is not None


def test_rejects_missing_status_code():
    line = "10.0.0.1 - - [22/Oct/2026:19:03:36 +0200] " '"GET / HTTP/1.1"'
    assert log_line_pattern.fullmatch(line) is None


def test_rejects_non_log_text():
    assert log_line_pattern.fullmatch("This is not a server log") is None


def test_rejects_missing_request_quotes():
    line = "10.0.0.1 - - [22/Oct/2026:19:03:36 +0200] " "GET / HTTP/1.1 200 123"
    assert log_line_pattern.fullmatch(line) is None
