import pytest

import src.main as main_module
from src.main import format_report, main


@pytest.fixture
def sample_report():
    return {
        "total_requests": 4,
        "unique_ips": 3,
        "total_bytes": 350,
        "error_requests": 2,
        "requests_by_method": {
            "GET": 2,
            "POST": 1,
            "DELETE": 1,
        },
        "status_counts": {
            200: 1,
            201: 1,
            404: 1,
            500: 1,
        },
        "requests_by_ip": {
            "192.168.1.10": 2,
            "192.168.1.11": 1,
            "192.168.1.12": 1,
        },
        "top_urls": [
            ("/", 1),
            ("/login", 1),
        ],
        "requests_by_hour": {},
    }


def test_format_report_has_heading(sample_report):
    text = format_report(sample_report, "data/access.log")

    assert text.startswith("LOG FILE ANALYSIS REPORT\n========================")


def test_format_report_includes_source(sample_report):
    text = format_report(sample_report, "data/access.log")
    assert "Source: data/access.log" in text


def test_format_report_includes_summary_counts(sample_report):
    text = format_report(sample_report, "data/access.log")

    assert "Total requests: 4" in text
    assert "Unique IP addresses: 3" in text
    assert "Total response bytes: 350" in text
    assert "Requests with 4xx/5xx status: 2" in text


def test_format_report_includes_methods_and_statuses(sample_report):
    text = format_report(sample_report, "data/access.log")

    assert "Requests by HTTP method:" in text
    assert "  GET: 2" in text
    assert "Requests by status code:" in text
    assert "  404: 1" in text


def test_format_report_includes_top_urls(sample_report):
    text = format_report(sample_report, "data/access.log")

    assert "Top URLs:" in text
    assert "  /: 1" in text
    assert "  /login: 1" in text


def test_format_report_has_generated_timestamp(sample_report):
    text = format_report(sample_report, "data/access.log")

    assert "Generated: " in text
    # The report should use a timezone offset such as +0200.
    generated_line = next(
        line for line in text.splitlines() if line.startswith("Generated: ")
    )
    assert len(generated_line.split("Generated: ", 1)[1]) >= 25


def test_main_writes_report_file(
    monkeypatch,
    tmp_path,
    sample_report,
    capsys,
):
    output_path = tmp_path / "reports" / "report.txt"

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "data/access.log",
            "--output",
            str(output_path),
        ],
    )
    monkeypatch.setattr(
        main_module,
        "analyze_files",
        lambda **kwargs: sample_report,
    )

    main()

    saved_text = output_path.read_text(encoding="utf-8")
    printed_text = capsys.readouterr().out

    assert "LOG FILE ANALYSIS REPORT" in saved_text
    assert "Source: data/access.log" in saved_text
    assert saved_text in printed_text


def test_main_passes_status_filter(
    monkeypatch,
    tmp_path,
    sample_report,
):
    captured = {}

    def fake_analyze_files(**kwargs):
        captured.update(kwargs)
        return sample_report

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "data/access.log",
            "--status",
            "404",
            "--output",
            str(tmp_path / "report.txt"),
        ],
    )
    monkeypatch.setattr(
        main_module,
        "analyze_files",
        fake_analyze_files,
    )

    main()

    assert captured["status_code"] == 404


def test_main_passes_ip_filter(
    monkeypatch,
    tmp_path,
    sample_report,
):
    captured = {}

    def fake_analyze_files(**kwargs):
        captured.update(kwargs)
        return sample_report

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "data/access.log",
            "--ip",
            "192.168.1.10",
            "--output",
            str(tmp_path / "report.txt"),
        ],
    )
    monkeypatch.setattr(
        main_module,
        "analyze_files",
        fake_analyze_files,
    )

    main()

    assert captured["ip_address"] == "192.168.1.10"


def test_analyze_files_combines_multiple_sources(
    monkeypatch,
    sample_entries,
):
    def fake_read_log_lines(path):
        return iter([str(path)])

    def fake_parse_log_line(line):
        return sample_entries[0] if line else None

    monkeypatch.setattr(
        main_module,
        "read_log_lines",
        fake_read_log_lines,
    )
    monkeypatch.setattr(
        main_module,
        "parse_log_line",
        fake_parse_log_line,
    )

    captured = {}

    def fake_generate_report(entries):
        captured["entries"] = list(entries)
        return {"total_requests": len(captured["entries"])}

    monkeypatch.setattr(
        main_module,
        "generate_report",
        fake_generate_report,
    )

    result = main_module.analyze_files(["first.log", "second.log"])

    assert result["total_requests"] == 2
    assert len(captured["entries"]) == 2
