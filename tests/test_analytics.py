
from datetime import timedelta

from src.analytics import (
    calculate_total_bytes,
    count_requests_by_ip,
    count_status_codes,
    find_top_urls,
    generate_report,
    group_entries_by_hour,
)


def test_count_status_codes(sample_entries):
    assert count_status_codes(sample_entries) == {
        200: 1,
        201: 1,
        404: 1,
        500: 1,
    }


def test_count_requests_by_ip(sample_entries):
    assert count_requests_by_ip(sample_entries) == {
        "192.168.1.10": 2,
        "192.168.1.11": 1,
        "192.168.1.12": 1,
    }


def test_find_top_urls(sample_entries):
    result = find_top_urls(sample_entries, limit=2)
    assert result == [("/", 1), ("/login", 1)]


def test_calculate_total_bytes(sample_entries):
    assert calculate_total_bytes(sample_entries) == 350


def test_calculate_total_bytes_empty():
    assert calculate_total_bytes([]) == 0


def test_group_entries_by_hour(sample_entries):
    result = group_entries_by_hour(sample_entries)

    first_hour = sample_entries[0].timestamp.replace(
        minute=0, second=0, microsecond=0
    )
    second_hour = first_hour + timedelta(hours=1)

    assert result[first_hour] == 3
    assert result[second_hour] == 1


def test_generate_report_total_requests(sample_entries):
    report = generate_report(sample_entries)
    assert report["total_requests"] == 4


def test_generate_report_unique_ips(sample_entries):
    report = generate_report(sample_entries)
    assert report["unique_ips"] == 3


def test_generate_report_error_count(sample_entries):
    report = generate_report(sample_entries)
    assert report["error_requests"] == 2


def test_generate_report_method_counts(sample_entries):
    report = generate_report(sample_entries)
    assert report["requests_by_method"] == {
        "GET": 2,
        "POST": 1,
        "DELETE": 1,
    }


def test_generate_report_empty_input():
    report = generate_report([])

    assert report["total_requests"] == 0
    assert report["unique_ips"] == 0
    assert report["total_bytes"] == 0
    assert report["error_requests"] == 0
    assert report["status_counts"] == {}
    assert report["requests_by_method"] == {}
    assert report["top_urls"] == []
    assert report["requests_by_hour"] == {}
