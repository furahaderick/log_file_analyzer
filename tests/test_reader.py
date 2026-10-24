import pytest

from src.reader import read_log_lines


def test_reads_all_lines(tmp_path, sample_log_lines):
    path = tmp_path / "access.log"
    path.write_text("\n".join(sample_log_lines), encoding="utf-8")

    assert list(read_log_lines(path)) == sample_log_lines


def test_reads_single_line(tmp_path, sample_log_line):
    path = tmp_path / "access.log"
    path.write_text(sample_log_line + "\n", encoding="utf-8")

    assert list(read_log_lines(path)) == [sample_log_line]


def test_empty_file_yields_no_lines(tmp_path):
    path = tmp_path / "empty.log"
    path.write_text("", encoding="utf-8")

    assert list(read_log_lines(path)) == []


def test_missing_file_raises_error(tmp_path):
    path = tmp_path / "missing.log"

    with pytest.raises(FileNotFoundError):
        list(read_log_lines(path))


def test_reader_is_iterable(tmp_path, sample_log_lines):
    path = tmp_path / "access.log"
    path.write_text("\n".join(sample_log_lines), encoding="utf-8")

    lines = read_log_lines(path)

    # The reader should return an iterable, not a pre-built list.
    assert iter(lines) is lines
    assert next(lines) == sample_log_lines[0]


def test_reads_file_without_trailing_newline(tmp_path, sample_log_line):
    path = tmp_path / "access.log"
    path.write_text(sample_log_line, encoding="utf-8")

    assert list(read_log_lines(path)) == [sample_log_line]


def test_preserves_line_order(tmp_path, sample_log_lines):
    path = tmp_path / "access.log"
    path.write_text("\n".join(sample_log_lines), encoding="utf-8")

    assert list(read_log_lines(path)) == sample_log_lines
