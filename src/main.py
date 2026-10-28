import argparse
from collections.abc import Iterator
from datetime import datetime
from itertools import chain
from pathlib import Path

from src.analytics import generate_report
from src.models import RequestLogEntry
from src.parser import parse_log_line
from src.pipeline import build_pipeline
from src.reader import read_log_lines


def iter_parsed_entries(
    path: str | Path,
) -> Iterator[RequestLogEntry]:
    """Yield valid parsed entries from a log file"""
    for line in read_log_lines(path):
        entry = parse_log_line(line)

        if entry is not None:
            yield entry


def analyze_files(
    paths: list[str],
    status_code: int | None = None,
    ip_address: str | None = None,
) -> dict:
    """Analyze one or more log files"""
    entries = chain.from_iterable(iter_parsed_entries(path) for path in paths)

    pipeline = build_pipeline(
        entries,
        status_code=status_code,
        ip_address=ip_address,
    )

    return generate_report(pipeline)


def format_report(report: dict, source: str) -> str:
    """Format report statistics as readable plain text"""
    generated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")

    lines = [
        "LOG FILE ANALYSIS REPORT",
        "========================",
        f"Source: {source}",
        f"Generated: {generated}",
        "",
        f"Total requests: {report['total_requests']}",
        f"Unique IP addresses: {report['unique_ips']}",
        f"Total response bytes: {report['total_bytes']}",
        f"Requests with 4xx/5xx status: {report['error_requests']}",
        "",
        "Requests by HTTP method:",
    ]

    for method, count in sorted(report["requests_by_method"].items()):
        lines.append(f"  {method}: {count}")

    lines.extend(
        [
            "",
            "Requests by status code:",
        ]
    )

    for status, count in sorted(report["status_counts"].items()):
        lines.append(f"  {status}: {count}")

    lines.extend(
        [
            "",
            "Top URLs:",
        ]
    )

    for url, count in report["top_urls"]:
        lines.append(f"  {url}: {count}")

    return "\n".join(lines)


def main() -> None:
    """Run the log analyzer."""
    parser = argparse.ArgumentParser(
        description="Analyze one or more server log files."
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="Paths to log files.",
    )
    parser.add_argument(
        "--status",
        type=int,
        help="Filter by HTTP status code.",
    )
    parser.add_argument(
        "--ip",
        help="Filter by IP address.",
    )
    parser.add_argument(
        "--output",
        default="reports/report.txt",
        help="Where to save the report.",
    )

    args = parser.parse_args()

    try:
        report = analyze_files(
            paths=args.files,
            status_code=args.status,
            ip_address=args.ip,
        )
    except OSError as error:
        parser.error(f"Could not read a log file: {error}")

    # Display all source paths when analyzing multiple files
    source = ", ".join(args.files)
    report_text = format_report(report, source)

    print(report_text)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
