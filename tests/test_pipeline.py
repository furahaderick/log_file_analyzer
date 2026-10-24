import pytest

from src.pipeline import (
    build_pipeline,
    combine_entries,
    filter_by_ip,
    filter_by_status,
    filter_by_time_range,
    filter_not_found,
    filter_server_error,
    limit_entries,
    take_entries_until,
    transform_entry,
)


def test_transform_normalizes_method_and_url(sample_entries):
    entry = transform_entry(sample_entries[0])
    assert entry.method == "GET"
    assert entry.url == "/"


def test_transform_does_not_mutate_original_entry(sample_entries):
    original = sample_entries[0]
    transform_entry(original)
    assert original.method == "GET"


def test_filter_by_status(sample_entries):
    result = list(filter_by_status(sample_entries, 404))
    assert len(result) == 1
    assert result[0].url == "/missing"


def test_filter_by_ip(sample_entries):
    result = list(filter_by_ip(sample_entries, "192.168.1.10"))
    assert len(result) == 2


def test_filter_by_time_range(sample_entries):
    start = sample_entries[0].timestamp
    end = sample_entries[1].timestamp

    result = list(filter_by_time_range(sample_entries, start, end))
    assert len(result) == 2


def test_build_pipeline_combines_filters(sample_entries):
    result = list(
        build_pipeline(
            sample_entries,
            status_code=200,
            ip_address="192.168.1.10",
        )
    )
    assert len(result) == 1
    assert result[0].url == "/"


def test_combine_entries(sample_entries):
    result = list(combine_entries(sample_entries[:2], sample_entries[2:]))
    assert result == sample_entries


def test_limit_entries_returns_only_requested_number(sample_entries):
    assert list(limit_entries(sample_entries, 2)) == sample_entries[:2]


def test_limit_entries_zero_returns_empty(sample_entries):
    assert not list(limit_entries(sample_entries, 0))


def test_limit_entries_rejects_negative_limit(sample_entries):
    with pytest.raises(ValueError):
        limit_entries(sample_entries, -1)


def test_take_entries_until_stops_after_cutoff(sample_entries):
    # The entries are chronological in this fixture
    cutoff = sample_entries[2].timestamp
    result = list(take_entries_until(sample_entries, cutoff))

    assert result == sample_entries[:3]


def test_take_entries_until_stops_at_first_later_timestamp(sample_entries):
    # The fourth entry is later than this cutoff
    cutoff = sample_entries[2].timestamp
    result = list(take_entries_until(sample_entries, cutoff))

    assert all(entry.timestamp <= cutoff for entry in result)
    assert len(result) == 3


def test_partial_filter_for_404(sample_entries):
    result = list(filter_not_found(sample_entries))
    assert [entry.status for entry in result] == [404]


def test_partial_filter_for_500(sample_entries):
    result = list(filter_server_error(sample_entries))
    assert [entry.status for entry in result] == [500]


def test_pipeline_with_no_filters_keeps_all_entries(sample_entries):
    assert len(list(build_pipeline(sample_entries))) == len(sample_entries)
